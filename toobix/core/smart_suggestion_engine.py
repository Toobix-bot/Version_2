"""
Smart Suggestion Engine - Phase 5.1
Dynamische KI-gesteuerte Vorschläge und adaptive Buttons
"""

import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class SuggestionContext:
    """Kontext für Suggestion-Generierung"""
    last_message: str
    ai_response: str
    user_history: List[str]
    current_activity: str
    time_of_day: str
    system_state: Dict[str, Any]
    available_functions: List[str]

@dataclass
class SmartSuggestion:
    """Einzelner Vorschlag"""
    id: str
    text: str
    action: str
    category: str
    priority: int  # 1-5, 5 = höchste Priorität
    icon: str
    tooltip: str
    context_relevance: float  # 0.0-1.0
    learning_weight: float = 1.0

@dataclass
class SuggestionGroup:
    """Gruppe von verwandten Vorschlägen"""
    name: str
    suggestions: List[SmartSuggestion]
    display_mode: str  # 'buttons', 'dropdown', 'grid'
    max_visible: int = 3

class SmartSuggestionEngine:
    """
    Intelligente Vorschlag-Engine die dynamisch
    passende Aktionen basierend auf Kontext vorschlägt
    """
    
    def __init__(self):
        self.learning_data = {}
        self.suggestion_patterns = {}
        self.user_preferences = {}
        self.context_analyzers = []
        
        # Basis-Suggestion-Kategorien
        self.base_suggestions = {
            'productivity': self._get_productivity_suggestions(),
            'system': self._get_system_suggestions(),
            'wellness': self._get_wellness_suggestions(),
            'learning': self._get_learning_suggestions(),
            'automation': self._get_automation_suggestions(),
            'creative': self._get_creative_suggestions()
        }
        
        self.pattern_matchers = self._init_pattern_matchers()
        
        logger.info("🎯 Smart Suggestion Engine initialisiert")
    
    def analyze_context(self, context: SuggestionContext) -> List[SuggestionGroup]:
        """Analysiert Kontext und generiert passende Vorschläge"""
        try:
            # 1. Kontext-Analyse
            context_analysis = self._analyze_message_context(context)
            
            # 2. Relevante Kategorien identifizieren
            relevant_categories = self._identify_relevant_categories(context, context_analysis)
            
            # 3. Suggestions für jede Kategorie generieren
            suggestion_groups = []
            for category in relevant_categories:
                suggestions = self._generate_category_suggestions(category, context, context_analysis)
                if suggestions:
                    group = SuggestionGroup(
                        name=category.title(),
                        suggestions=suggestions,
                        display_mode='buttons' if len(suggestions) <= 3 else 'dropdown'
                    )
                    suggestion_groups.append(group)
            
            # 4. Nach Relevanz sortieren
            suggestion_groups = self._prioritize_groups(suggestion_groups, context)
            
            # 5. Lern-Daten aktualisieren
            self._update_learning_data(context, suggestion_groups)
            
            return suggestion_groups[:4]  # Max 4 Gruppen
            
        except Exception as e:
            logger.error(f"Suggestion-Analyse Fehler: {e}")
            return self._get_fallback_suggestions()
    
    def _analyze_message_context(self, context: SuggestionContext) -> Dict[str, Any]:
        """Analysiert die Nachricht um Kontext zu verstehen"""
        analysis = {
            'intent': 'unknown',
            'emotion': 'neutral',
            'complexity': 'medium',
            'action_needed': False,
            'keywords': [],
            'entities': [],
            'urgency': 'normal'
        }
        
        message = context.last_message.lower()
        response = context.ai_response.lower()
        
        # Intent-Erkennung
        intent_patterns = {
            'question': ['was', 'wie', 'wann', 'wo', 'warum', '?'],
            'request': ['bitte', 'kannst du', 'könntest du', 'mach', 'zeig'],
            'problem': ['fehler', 'problem', 'geht nicht', 'funktioniert nicht'],
            'exploration': ['zeig mir', 'erkläre', 'was kann', 'hilfe'],
            'automation': ['automatisch', 'regelmäßig', 'immer wenn', 'schedule']
        }
        
        for intent, patterns in intent_patterns.items():
            if any(pattern in message for pattern in patterns):
                analysis['intent'] = intent
                break
        
        # Emotion-Erkennung
        emotion_patterns = {
            'frustrated': ['ärgerlich', 'nervt', 'geht nicht', 'fehler'],
            'curious': ['interessant', 'spannend', 'mehr davon', 'cool'],
            'satisfied': ['perfekt', 'super', 'toll', 'danke'],
            'confused': ['verstehe nicht', 'unclear', 'verwirrend']
        }
        
        for emotion, patterns in emotion_patterns.items():
            if any(pattern in message or pattern in response for pattern in patterns):
                analysis['emotion'] = emotion
                break
        
        # Keyword-Extraktion
        important_keywords = re.findall(r'\b\w{4,}\b', message)
        analysis['keywords'] = list(set(important_keywords))[:10]
        
        # Action-Detection
        action_words = ['starte', 'öffne', 'organisiere', 'analysiere', 'erstelle', 'lösche']
        analysis['action_needed'] = any(word in message for word in action_words)
        
        return analysis
    
    def _identify_relevant_categories(self, context: SuggestionContext, analysis: Dict[str, Any]) -> List[str]:
        """Identifiziert relevante Suggestion-Kategorien"""
        categories = []
        
        # Basis-Kategorien basierend auf Intent
        intent_mapping = {
            'question': ['learning', 'system'],
            'request': ['productivity', 'automation'],
            'problem': ['system', 'learning'],
            'exploration': ['learning', 'creative'],
            'automation': ['automation', 'productivity']
        }
        
        intent = analysis.get('intent', 'unknown')
        if intent in intent_mapping:
            categories.extend(intent_mapping[intent])
        
        # Keyword-basierte Kategorien
        keyword_mapping = {
            'system': ['system', 'performance', 'monitor', 'status'],
            'wellness': ['meditation', 'pause', 'wellness', 'entspannung'],
            'productivity': ['organisation', 'task', 'aufgabe', 'produktiv'],
            'creative': ['kreativ', 'story', 'idee', 'brainstorm'],
            'learning': ['lernen', 'tutorial', 'hilfe', 'erklär']
        }
        
        for category, keywords in keyword_mapping.items():
            if any(keyword in ' '.join(analysis['keywords']).lower() for keyword in keywords):
                if category not in categories:
                    categories.append(category)
        
        # Zeitbasierte Kategorien
        hour = datetime.now().hour
        if 9 <= hour <= 17:  # Arbeitszeit
            if 'productivity' not in categories:
                categories.append('productivity')
        elif 18 <= hour <= 22:  # Abend
            if 'wellness' not in categories:
                categories.append('wellness')
        
        # Fallback
        if not categories:
            categories = ['productivity', 'system']
        
        return categories[:3]  # Max 3 Kategorien
    
    def _generate_category_suggestions(self, category: str, context: SuggestionContext, analysis: Dict[str, Any]) -> List[SmartSuggestion]:
        """Generiert Suggestions für eine spezifische Kategorie"""
        base_suggestions = self.base_suggestions.get(category, [])
        suggestions = []
        
        # Basis-Suggestions filtern und anpassen
        for suggestion_template in base_suggestions:
            # Relevanz basierend auf Kontext berechnen
            relevance = self._calculate_relevance(suggestion_template, context, analysis)
            
            if relevance > 0.3:  # Mindest-Relevanz
                suggestion = SmartSuggestion(
                    id=f"{category}_{suggestion_template['id']}",
                    text=suggestion_template['text'],
                    action=suggestion_template['action'],
                    category=category,
                    priority=suggestion_template['priority'],
                    icon=suggestion_template['icon'],
                    tooltip=suggestion_template['tooltip'],
                    context_relevance=relevance
                )
                suggestions.append(suggestion)
        
        # Dynamische Suggestions basierend auf Kontext
        dynamic_suggestions = self._generate_dynamic_suggestions(category, context, analysis)
        suggestions.extend(dynamic_suggestions)
        
        # Nach Relevanz und Priorität sortieren
        suggestions.sort(key=lambda s: (s.context_relevance * s.priority), reverse=True)
        
        return suggestions[:5]  # Max 5 Suggestions pro Kategorie
    
    def _calculate_relevance(self, suggestion_template: Dict[str, Any], context: SuggestionContext, analysis: Dict[str, Any]) -> float:
        """Berechnet Relevanz eines Vorschlags für den aktuellen Kontext"""
        relevance = 0.5  # Basis-Relevanz
        
        # Keyword-Matching
        suggestion_keywords = suggestion_template.get('keywords', [])
        context_keywords = analysis.get('keywords', [])
        
        keyword_matches = len(set(suggestion_keywords) & set(context_keywords))
        if keyword_matches > 0:
            relevance += 0.3 * (keyword_matches / len(suggestion_keywords))
        
        # Intent-Matching
        if suggestion_template.get('intent') == analysis.get('intent'):
            relevance += 0.2
        
        # Zeitbasierte Relevanz
        time_relevance = suggestion_template.get('time_relevance', {})
        current_hour = datetime.now().hour
        
        if 'preferred_hours' in time_relevance:
            if current_hour in time_relevance['preferred_hours']:
                relevance += 0.1
        
        # Benutzer-Präferenzen
        user_pref = self.user_preferences.get(suggestion_template['id'], 0.5)
        relevance = (relevance + user_pref) / 2
        
        return min(relevance, 1.0)
    
    def _generate_dynamic_suggestions(self, category: str, context: SuggestionContext, analysis: Dict[str, Any]) -> List[SmartSuggestion]:
        """Generiert dynamische Suggestions basierend auf aktuellem Kontext"""
        dynamic_suggestions = []
        
        if category == 'productivity':
            # Wenn Problem erwähnt wurde, schlage Lösung vor
            if analysis['emotion'] == 'frustrated':
                dynamic_suggestions.append(SmartSuggestion(
                    id="dynamic_problem_solve",
                    text="Problem analysieren",
                    action="analyze_current_problem",
                    category="productivity",
                    priority=5,
                    icon="🔍",
                    tooltip="Lass mich das Problem strukturiert analysieren",
                    context_relevance=0.9
                ))
        
        elif category == 'system':
            # System-Status vorschlagen wenn Performance erwähnt
            if any(word in context.last_message.lower() for word in ['langsam', 'performance', 'system']):
                dynamic_suggestions.append(SmartSuggestion(
                    id="dynamic_system_check",
                    text="System-Check starten",
                    action="deep_system_analysis",
                    category="system",
                    priority=4,
                    icon="⚡",
                    tooltip="Vollständige System-Analyse durchführen",
                    context_relevance=0.8
                ))
        
        elif category == 'learning':
            # Tutorial vorschlagen basierend auf Kontext
            if analysis['intent'] == 'question':
                dynamic_suggestions.append(SmartSuggestion(
                    id="dynamic_tutorial",
                    text="Erklärungs-Modus",
                    action="enter_explanation_mode",
                    category="learning",
                    priority=3,
                    icon="📚",
                    tooltip="Detaillierte Erklärungen für alle Schritte",
                    context_relevance=0.7
                ))
        
        return dynamic_suggestions
    
    def _prioritize_groups(self, groups: List[SuggestionGroup], context: SuggestionContext) -> List[SuggestionGroup]:
        """Priorisiert Suggestion-Gruppen basierend auf Kontext"""
        def group_score(group: SuggestionGroup) -> float:
            if not group.suggestions:
                return 0.0
            
            # Durchschnittliche Relevanz der Suggestions
            avg_relevance = sum(s.context_relevance for s in group.suggestions) / len(group.suggestions)
            
            # Maximale Priorität in der Gruppe
            max_priority = max(s.priority for s in group.suggestions)
            
            # Zeitbasierte Gewichtung
            time_weight = 1.0
            hour = datetime.now().hour
            
            if group.name.lower() == 'wellness' and 18 <= hour <= 22:
                time_weight = 1.3
            elif group.name.lower() == 'productivity' and 9 <= hour <= 17:
                time_weight = 1.2
            
            return (avg_relevance * max_priority * time_weight) / 5.0
        
        groups.sort(key=group_score, reverse=True)
        return groups
    
    def _update_learning_data(self, context: SuggestionContext, groups: List[SuggestionGroup]):
        """Aktualisiert Lern-Daten für zukünftige Verbesserungen"""
        timestamp = datetime.now().isoformat()
        
        learning_entry = {
            'timestamp': timestamp,
            'context_intent': context.current_activity,
            'generated_groups': len(groups),
            'group_names': [g.name for g in groups],
            'total_suggestions': sum(len(g.suggestions) for g in groups)
        }
        
        # Speichere für spätere Analyse
        if 'suggestion_history' not in self.learning_data:
            self.learning_data['suggestion_history'] = []
        
        self.learning_data['suggestion_history'].append(learning_entry)
        
        # Behalte nur letzte 100 Einträge
        self.learning_data['suggestion_history'] = self.learning_data['suggestion_history'][-100:]
    
    def update_user_feedback(self, suggestion_id: str, action: str):
        """Aktualisiert Benutzer-Feedback für Lern-Algorithmus"""
        if suggestion_id not in self.user_preferences:
            self.user_preferences[suggestion_id] = 0.5
        
        # Feedback-basierte Anpassung
        if action == 'clicked':
            self.user_preferences[suggestion_id] = min(1.0, self.user_preferences[suggestion_id] + 0.1)
        elif action == 'dismissed':
            self.user_preferences[suggestion_id] = max(0.1, self.user_preferences[suggestion_id] - 0.05)
        elif action == 'ignored':
            self.user_preferences[suggestion_id] = max(0.2, self.user_preferences[suggestion_id] - 0.02)
    
    def _get_fallback_suggestions(self) -> List[SuggestionGroup]:
        """Standard-Suggestions wenn Analyse fehlschlägt"""
        fallback_suggestions = [
            SmartSuggestion(
                id="fallback_help",
                text="Hilfe anzeigen",
                action="show_help",
                category="system",
                priority=3,
                icon="❓",
                tooltip="Zeige verfügbare Funktionen",
                context_relevance=0.5
            ),
            SmartSuggestion(
                id="fallback_status",
                text="System-Status",
                action="system_status",
                category="system", 
                priority=2,
                icon="📊",
                tooltip="Aktueller System-Status",
                context_relevance=0.4
            )
        ]
        
        return [SuggestionGroup(
            name="Standard",
            suggestions=fallback_suggestions,
            display_mode="buttons"
        )]
    
    def _get_productivity_suggestions(self) -> List[Dict[str, Any]]:
        """Basis-Productivity Suggestions"""
        return [
            {
                'id': 'organize_desktop',
                'text': 'Desktop organisieren',
                'action': 'organize_desktop',
                'priority': 4,
                'icon': '🗂️',
                'tooltip': 'Sortiere Desktop-Dateien automatisch',
                'keywords': ['desktop', 'organisation', 'dateien'],
                'intent': 'request',
                'time_relevance': {'preferred_hours': list(range(9, 18))}
            },
            {
                'id': 'focus_mode',
                'text': 'Fokus-Modus',
                'action': 'enter_focus_mode',
                'priority': 5,
                'icon': '🎯',
                'tooltip': 'Aktiviere Konzentrations-Unterstützung',
                'keywords': ['fokus', 'konzentration', 'arbeit'],
                'intent': 'request'
            },
            {
                'id': 'task_reminder',
                'text': 'Aufgaben-Reminder',
                'action': 'setup_task_reminder',
                'priority': 3,
                'icon': '⏰',
                'tooltip': 'Setze Erinnerungen für wichtige Aufgaben',
                'keywords': ['aufgabe', 'reminder', 'erinnerung'],
                'intent': 'automation'
            },
            {
                'id': 'productivity_report',
                'text': 'Produktivitäts-Report',
                'action': 'generate_productivity_report',
                'priority': 2,
                'icon': '📈',
                'tooltip': 'Zeige heutige Produktivitäts-Statistiken',
                'keywords': ['produktivität', 'statistik', 'report'],
                'intent': 'question'
            }
        ]
    
    def _get_system_suggestions(self) -> List[Dict[str, Any]]:
        """Basis-System Suggestions"""
        return [
            {
                'id': 'system_health',
                'text': 'System-Gesundheit',
                'action': 'deep_system_analysis',
                'priority': 4,
                'icon': '🏥',
                'tooltip': 'Vollständige System-Analyse durchführen',
                'keywords': ['system', 'gesundheit', 'analyse'],
                'intent': 'question'
            },
            {
                'id': 'optimize_performance',
                'text': 'Performance optimieren',
                'action': 'optimize_system_performance',
                'priority': 5,
                'icon': '⚡',
                'tooltip': 'Automatische System-Optimierung',
                'keywords': ['performance', 'optimierung', 'beschleunigung'],
                'intent': 'request'
            },
            {
                'id': 'security_scan',
                'text': 'Sicherheits-Scan',
                'action': 'security_scan',
                'priority': 3,
                'icon': '🔒',
                'tooltip': 'Prüfe System auf Sicherheitslücken',
                'keywords': ['sicherheit', 'scan', 'schutz'],
                'intent': 'request'
            }
        ]
    
    def _get_wellness_suggestions(self) -> List[Dict[str, Any]]:
        """Basis-Wellness Suggestions"""
        return [
            {
                'id': 'meditation_break',
                'text': '5-Min Meditation',
                'action': 'start_meditation_5min',
                'priority': 4,
                'icon': '🧘',
                'tooltip': 'Kurze Meditations-Pause einlegen',
                'keywords': ['meditation', 'pause', 'entspannung'],
                'intent': 'request',
                'time_relevance': {'preferred_hours': list(range(14, 20))}
            },
            {
                'id': 'breathing_exercise',
                'text': 'Atemübung',
                'action': 'start_breathing_exercise',
                'priority': 3,
                'icon': '🫁',
                'tooltip': 'Geführte Atemübung zur Entspannung',
                'keywords': ['atmung', 'entspannung', 'stress'],
                'intent': 'request'
            },
            {
                'id': 'posture_check',
                'text': 'Haltungs-Check',
                'action': 'posture_reminder',
                'priority': 2,
                'icon': '🪑',
                'tooltip': 'Erinnerung für bessere Sitzposition',
                'keywords': ['haltung', 'ergonomie', 'gesundheit'],
                'intent': 'automation'
            }
        ]
    
    def _get_learning_suggestions(self) -> List[Dict[str, Any]]:
        """Basis-Learning Suggestions"""
        return [
            {
                'id': 'explore_features',
                'text': 'Features erkunden',
                'action': 'feature_exploration_mode',
                'priority': 3,
                'icon': '🔍',
                'tooltip': 'Entdecke neue Toobix-Funktionen',
                'keywords': ['features', 'funktionen', 'entdecken'],
                'intent': 'exploration'
            },
            {
                'id': 'tutorial_mode',
                'text': 'Tutorial-Modus',
                'action': 'enter_tutorial_mode',
                'priority': 4,
                'icon': '🎓',
                'tooltip': 'Schritt-für-Schritt Anleitungen',
                'keywords': ['tutorial', 'anleitung', 'lernen'],
                'intent': 'question'
            },
            {
                'id': 'tips_and_tricks',
                'text': 'Tipps & Tricks',
                'action': 'show_tips_and_tricks',
                'priority': 2,
                'icon': '💡',
                'tooltip': 'Praktische Tipps für bessere Nutzung',
                'keywords': ['tipps', 'tricks', 'hilfe'],
                'intent': 'exploration'
            }
        ]
    
    def _get_automation_suggestions(self) -> List[Dict[str, Any]]:
        """Basis-Automation Suggestions"""
        return [
            {
                'id': 'auto_organize',
                'text': 'Auto-Organisation',
                'action': 'setup_auto_organization',
                'priority': 4,
                'icon': '🤖',
                'tooltip': 'Automatische Datei-Organisation einrichten',
                'keywords': ['automatisch', 'organisation', 'schedule'],
                'intent': 'automation'
            },
            {
                'id': 'smart_reminders',
                'text': 'Smarte Erinnerungen',
                'action': 'setup_smart_reminders',
                'priority': 3,
                'icon': '🔔',
                'tooltip': 'KI-basierte Erinnerungen erstellen',
                'keywords': ['erinnerung', 'smart', 'automatisch'],
                'intent': 'automation'
            },
            {
                'id': 'routine_automation',
                'text': 'Routine automatisieren',
                'action': 'create_automation_routine',
                'priority': 5,
                'icon': '⚙️',
                'tooltip': 'Tägliche Routinen automatisieren',
                'keywords': ['routine', 'automatisierung', 'täglich'],
                'intent': 'automation'
            }
        ]
    
    def _get_creative_suggestions(self) -> List[Dict[str, Any]]:
        """Basis-Creative Suggestions"""
        return [
            {
                'id': 'story_mode',
                'text': 'Story-Modus',
                'action': 'enter_story_mode',
                'priority': 4,
                'icon': '📖',
                'tooltip': 'Interaktive Geschichten erleben',
                'keywords': ['story', 'geschichte', 'kreativ'],
                'intent': 'exploration'
            },
            {
                'id': 'brainstorm_session',
                'text': 'Brainstorming',
                'action': 'start_brainstorm_session',
                'priority': 3,
                'icon': '💭',
                'tooltip': 'Kreative Ideenfindung mit KI',
                'keywords': ['brainstorm', 'ideen', 'kreativ'],
                'intent': 'request'
            },
            {
                'id': 'creative_writing',
                'text': 'Kreatives Schreiben',
                'action': 'creative_writing_assistant',
                'priority': 2,
                'icon': '✍️',
                'tooltip': 'Unterstützung beim kreativen Schreiben',
                'keywords': ['schreiben', 'kreativ', 'text'],
                'intent': 'request'
            }
        ]
    
    def _init_pattern_matchers(self) -> Dict[str, Any]:
        """Initialisiert Pattern-Matcher für verschiedene Kontexte"""
        return {
            'time_patterns': {
                'morning': list(range(6, 12)),
                'afternoon': list(range(12, 18)),
                'evening': list(range(18, 24)),
                'night': list(range(0, 6))
            },
            'activity_patterns': {
                'work': ['arbeit', 'job', 'projekt', 'task', 'aufgabe'],
                'learn': ['lernen', 'verstehen', 'erklären', 'tutorial'],
                'relax': ['entspannen', 'pause', 'ruhe', 'stress'],
                'organize': ['organisieren', 'aufräumen', 'sortieren']
            }
        }
    
    def get_suggestion_analytics(self) -> Dict[str, Any]:
        """Gibt Analyse-Daten über Suggestion-Performance zurück"""
        if 'suggestion_history' not in self.learning_data:
            return {'error': 'Keine Daten verfügbar'}
        
        history = self.learning_data['suggestion_history']
        
        analytics = {
            'total_suggestions_generated': sum(entry['total_suggestions'] for entry in history),
            'average_groups_per_session': sum(entry['generated_groups'] for entry in history) / len(history) if history else 0,
            'most_common_categories': {},
            'user_preference_trends': dict(self.user_preferences),
            'suggestion_frequency': len(history)
        }
        
        # Kategorie-Häufigkeit
        all_categories = []
        for entry in history:
            all_categories.extend(entry['group_names'])
        
        from collections import Counter
        category_counts = Counter(all_categories)
        analytics['most_common_categories'] = dict(category_counts.most_common(5))
        
        return analytics
