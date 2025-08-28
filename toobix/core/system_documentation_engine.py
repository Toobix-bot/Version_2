"""
Toobix System Documentation & Function Explorer
Vollständige Dokumentation aller Features und System-Komponenten
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SystemComponent:
    """System-Komponente"""
    name: str
    description: str
    status: str  # active, inactive, error
    version: str
    features: List[str]
    dependencies: List[str]
    commands: List[str]
    config_options: Dict[str, Any]

@dataclass
class FunctionDocumentation:
    """Funktions-Dokumentation"""
    function_name: str
    category: str
    description: str
    usage: str
    examples: List[str]
    parameters: List[str]
    return_type: str
    complexity: str  # beginner, intermediate, advanced
    status: str  # working, experimental, disabled

class SystemDocumentationEngine:
    """
    System-Dokumentations-Engine für vollständige Transparenz
    """
    
    def __init__(self):
        """Initialisiert Documentation Engine"""
        self.system_components = {}
        self.function_docs = {}
        self.tutorials = {}
        self.system_status = {}
        
        # Datenverzeichnis
        self.data_dir = Path('toobix_documentation')
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialisierung
        self._initialize_system_components()
        self._initialize_function_documentation()
        self._initialize_tutorials()
        
        logger.info("📚 System Documentation Engine initialisiert")
    
    def _initialize_system_components(self) -> None:
        """Initialisiert System-Komponenten-Dokumentation"""
        components = {
            'ai_handler': SystemComponent(
                name="AI Handler",
                description="Hybrid KI-System mit Ollama (lokal) und Groq (Cloud) Integration",
                status="active",
                version="3.0",
                features=[
                    "Intelligente KI-Weiterleitung",
                    "Lokale Ollama Integration (gemma2:2b)",
                    "Groq Cloud Backup (llama-3.1-8b-instant)",
                    "Kontext-bewusste Antworten",
                    "Automatisches Fallback-System"
                ],
                dependencies=["ollama", "groq", "requests", "aiohttp"],
                commands=[
                    "Alle Chat-Eingaben",
                    "KI-Abfragen",
                    "Kontext-Integration"
                ],
                config_options={
                    "ollama_url": "http://localhost:11434",
                    "ollama_model": "gemma2:2b",
                    "groq_model": "llama-3.1-8b-instant",
                    "cloud_threshold": 500,
                    "timeout": 30
                }
            ),
            
            'speech_engine': SystemComponent(
                name="Speech Engine",
                description="Fortgeschrittene Spracherkennung und Text-to-Speech",
                status="active",
                version="2.5",
                features=[
                    "Wake-Word Detection (Hey Toobix)",
                    "Kontinuierliche Spracherkennung",
                    "Deutsche TTS-Ausgabe",
                    "Mikrofon-Kalibrierung",
                    "Geräuschunterdrückung"
                ],
                dependencies=["speech_recognition", "pyttsx3", "pyaudio"],
                commands=[
                    "'Hey Toobix' + Sprachbefehl",
                    "Push-to-Talk (Leertaste)",
                    "Sprach-Toggle"
                ],
                config_options={
                    "wake_word": "hey toobix",
                    "language": "de-DE",
                    "tts_rate": 200,
                    "energy_threshold": 300
                }
            ),
            
            'context_manager': SystemComponent(
                name="Intelligent Context Manager",
                description="KI-basierte Arbeitskontext-Erkennung und Produktivitäts-Optimierung",
                status="active",
                version="1.0",
                features=[
                    "Automatische Kontext-Erkennung",
                    "Produktivitäts-Metriken",
                    "Energy-Level Tracking",
                    "Stress-Indikatoren",
                    "Intelligente Pausen-Empfehlungen"
                ],
                dependencies=["psutil", "pathlib"],
                commands=[
                    "'context analytics'",
                    "Automatisches Monitoring"
                ],
                config_options={
                    "monitoring_interval": 30,
                    "data_retention": 1000,
                    "confidence_threshold": 0.7
                }
            ),
            
            'gamification': SystemComponent(
                name="Productivity Gamification",
                description="XP-System und Achievement-Engine für Motivation",
                status="active",
                version="1.0",
                features=[
                    "XP-System mit Level-Progression",
                    "50+ verschiedene Achievements",
                    "Daily Challenges (KI-generiert)",
                    "Produktivitäts-Streaks",
                    "Motivations-Engine"
                ],
                dependencies=["random", "statistics"],
                commands=[
                    "'gamification'",
                    "'level up'",
                    "'achievements'"
                ],
                config_options={
                    "xp_multiplier": 1.0,
                    "daily_challenges": 3,
                    "achievement_notifications": True
                }
            ),
            
            'analytics_engine': SystemComponent(
                name="Deep Analytics Engine",
                description="Machine Learning für Produktivitäts-Pattern und Vorhersagen",
                status="active",
                version="1.0",
                features=[
                    "Verhaltens-Pattern Analyse",
                    "Performance-Vorhersagen",
                    "Korrelations-Analyse",
                    "Optimierungs-Empfehlungen",
                    "Predictive Insights"
                ],
                dependencies=["numpy", "pandas", "statistics"],
                commands=[
                    "'deep analytics'",
                    "'productivity patterns'",
                    "'analytics dashboard'"
                ],
                config_options={
                    "min_data_points": 10,
                    "prediction_horizon": 24,
                    "learning_rate": 0.1
                }
            ),
            
            'wellness_engine': SystemComponent(
                name="Creative Wellness Engine",
                description="Ganzheitliches Wellness-System mit Meditation und Soundscapes",
                status="active",
                version="1.0",
                features=[
                    "5 Adaptive Soundscapes",
                    "Geführte Meditation-Sessions",
                    "Atemübungen (3 Patterns)",
                    "Biofeedback-Simulation",
                    "Stress-Level Monitoring"
                ],
                dependencies=["threading", "random"],
                commands=[
                    "'wellness dashboard'",
                    "'start meditation'",
                    "'start breathing'",
                    "'focus sounds'"
                ],
                config_options={
                    "binaural_beats": True,
                    "nature_sounds_volume": 0.6,
                    "meditation_reminder": 120,
                    "stress_threshold": 70
                }
            ),
            
            'git_integration': SystemComponent(
                name="Git Integration Manager",
                description="Intelligente Git-Repository-Verwaltung und Bulk-Operationen",
                status="active",
                version="2.0",
                features=[
                    "Automatische Repository-Erkennung",
                    "Bulk Git-Operationen",
                    "Repository-Gesundheits-Dashboard",
                    "Programmiersprachen-Analyse",
                    "Commit-Automatisierung"
                ],
                dependencies=["subprocess", "pathlib"],
                commands=[
                    "'git scan'",
                    "'git dashboard'",
                    "'git pull all'",
                    "'git push all'"
                ],
                config_options={
                    "scan_depth": 5,
                    "auto_commit": False,
                    "health_threshold": 80
                }
            ),
            
            'task_scheduler': SystemComponent(
                name="Intelligent Task Scheduler",
                description="Event-basierte Automatisierung mit Regel-Engine",
                status="active",
                version="2.0",
                features=[
                    "Event-basierte Trigger",
                    "Regel-Engine",
                    "Automatisierte Aktionen",
                    "Backup-Automatisierung",
                    "System-Event Monitoring"
                ],
                dependencies=["threading", "subprocess"],
                commands=[
                    "'create rule'",
                    "'automation dashboard'",
                    "'show rules'"
                ],
                config_options={
                    "check_interval": 60,
                    "max_concurrent_rules": 10,
                    "rule_timeout": 300
                }
            ),
            
            'system_monitor': SystemComponent(
                name="Advanced System Monitor",
                description="Enterprise-grade System-Überwachung mit Predictive Analytics",
                status="active",
                version="2.0",
                features=[
                    "Echtzeit Performance-Monitoring",
                    "System-Gesundheits-Scores",
                    "Predictive Maintenance",
                    "Performance-Alerts",
                    "Ressourcen-Optimierung"
                ],
                dependencies=["psutil", "threading"],
                commands=[
                    "'system monitor'",
                    "'performance report'",
                    "'system health'"
                ],
                config_options={
                    "monitoring_interval": 5,
                    "alert_thresholds": {"cpu": 80, "memory": 85, "disk": 90},
                    "history_retention": 1440
                }
            )
        }
        
        self.system_components.update(components)
    
    def _initialize_function_documentation(self) -> None:
        """Initialisiert Funktions-Dokumentation"""
        functions = [
            # AI & Chat Functions
            FunctionDocumentation(
                function_name="Chat mit KI",
                category="AI & Kommunikation",
                description="Intelligente Unterhaltung mit Hybrid-KI-System",
                usage="Einfach Text eingeben oder 'Hey Toobix' sagen",
                examples=[
                    "Hallo Toobix, wie geht es dir?",
                    "Erkläre mir Python",
                    "Was ist Machine Learning?"
                ],
                parameters=["Beliebiger Text"],
                return_type="KI-Antwort",
                complexity="beginner",
                status="working"
            ),
            
            # System Management
            FunctionDocumentation(
                function_name="system monitor",
                category="System-Verwaltung",
                description="Erweiterte System-Überwachung mit Gesundheits-Scores",
                usage="'system monitor' oder 'performance report'",
                examples=[
                    "system monitor",
                    "performance report",
                    "system health"
                ],
                parameters=["Kein Parameter"],
                return_type="System-Übersicht",
                complexity="intermediate",
                status="working"
            ),
            
            FunctionDocumentation(
                function_name="git integration",
                category="Entwicklung",
                description="Git-Repository-Management und Bulk-Operationen",
                usage="'git scan' für Repository-Übersicht",
                examples=[
                    "git scan",
                    "git dashboard",
                    "git pull all",
                    "git push all"
                ],
                parameters=["Git-Operation"],
                return_type="Git-Status",
                complexity="intermediate",
                status="working"
            ),
            
            # Productivity Features
            FunctionDocumentation(
                function_name="gamification",
                category="Produktivität",
                description="XP-System und Achievement-Tracking für Motivation",
                usage="'gamification' für Dashboard",
                examples=[
                    "gamification",
                    "level up",
                    "achievements",
                    "xp dashboard"
                ],
                parameters=["Kein Parameter"],
                return_type="Gamification-Dashboard",
                complexity="beginner",
                status="working"
            ),
            
            FunctionDocumentation(
                function_name="context analytics",
                category="KI-Enhanced",
                description="Intelligente Arbeitskontext-Erkennung und Optimierung",
                usage="'context analytics' für Kontext-Analyse",
                examples=[
                    "context analytics",
                    "working context",
                    "kontext analyse"
                ],
                parameters=["Kein Parameter"],
                return_type="Kontext-Übersicht",
                complexity="advanced",
                status="working"
            ),
            
            FunctionDocumentation(
                function_name="deep analytics",
                category="Machine Learning",
                description="ML-basierte Produktivitäts-Pattern und Vorhersagen",
                usage="'deep analytics' für ML-Insights",
                examples=[
                    "deep analytics",
                    "productivity patterns",
                    "analytics dashboard"
                ],
                parameters=["Kein Parameter"],
                return_type="Analytics-Dashboard",
                complexity="advanced",
                status="working"
            ),
            
            # Wellness Features
            FunctionDocumentation(
                function_name="wellness system",
                category="Wellness",
                description="Ganzheitliches Wellness-System mit Meditation und Sounds",
                usage="'wellness dashboard' oder spezifische Aktionen",
                examples=[
                    "wellness dashboard",
                    "start meditation",
                    "start breathing",
                    "focus sounds",
                    "zen garden"
                ],
                parameters=["Wellness-Aktion"],
                return_type="Wellness-Status",
                complexity="beginner",
                status="working"
            ),
            
            # File & System Organization
            FunctionDocumentation(
                function_name="file organization",
                category="Organisation",
                description="Intelligente Datei-Organisation und System-Aufräumung",
                usage="'organize files' oder 'system cleanup'",
                examples=[
                    "organize my files",
                    "clean system",
                    "organize desktop",
                    "master organization"
                ],
                parameters=["Organisations-Typ"],
                return_type="Organisations-Bericht",
                complexity="intermediate",
                status="working"
            ),
            
            # Automation
            FunctionDocumentation(
                function_name="automation rules",
                category="Automatisierung",
                description="Event-basierte Automatisierung und Regel-Erstellung",
                usage="'create rule' oder 'automation dashboard'",
                examples=[
                    "create daily backup rule",
                    "automation dashboard",
                    "show rules"
                ],
                parameters=["Regel-Typ"],
                return_type="Automatisierungs-Status",
                complexity="advanced",
                status="working"
            ),
            
            # Speech & Voice
            FunctionDocumentation(
                function_name="voice control",
                category="Sprachsteuerung",
                description="Wake-Word Detection und Sprachbefehle",
                usage="'Hey Toobix' + Befehl oder Leertaste drücken",
                examples=[
                    "Hey Toobix, wie ist das Wetter?",
                    "[Leertaste drücken] Was ist die Zeit?",
                    "Sprach-Toggle aktivieren"
                ],
                parameters=["Sprachbefehl"],
                return_type="Sprach-Antwort",
                complexity="beginner",
                status="working"
            )
        ]
        
        for func in functions:
            self.function_docs[func.function_name] = func
    
    def _initialize_tutorials(self) -> None:
        """Initialisiert Tutorial-System"""
        tutorials = {
            'getting_started': {
                'title': '🚀 Erste Schritte mit Toobix',
                'description': 'Grundlagen und wichtigste Features',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Chat mit der KI',
                        'description': 'Tippe einfach eine Frage in das Chat-Feld',
                        'example': 'Hallo Toobix, erkläre mir deine Features',
                        'expected_result': 'KI-Antwort mit Feature-Übersicht'
                    },
                    {
                        'step': 2,
                        'title': 'Sprachsteuerung aktivieren',
                        'description': 'Sage "Hey Toobix" oder drücke die Leertaste',
                        'example': 'Hey Toobix, wie ist die Uhrzeit?',
                        'expected_result': 'Sprachantwort mit aktueller Zeit'
                    },
                    {
                        'step': 3,
                        'title': 'System-Monitoring',
                        'description': 'Überwache dein System in Echtzeit',
                        'example': 'system monitor',
                        'expected_result': 'Detaillierte System-Übersicht'
                    },
                    {
                        'step': 4,
                        'title': 'Produktivitäts-Gamification',
                        'description': 'Steigere deine Motivation mit XP und Achievements',
                        'example': 'gamification',
                        'expected_result': 'XP-Dashboard mit Level und Achievements'
                    }
                ]
            },
            
            'advanced_features': {
                'title': '🧠 Erweiterte KI-Features',
                'description': 'KI-Enhanced Features und Deep Analytics',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Context Analytics',
                        'description': 'Lass die KI deinen Arbeitskontext analysieren',
                        'example': 'context analytics',
                        'expected_result': 'Intelligente Kontext-Analyse'
                    },
                    {
                        'step': 2,
                        'title': 'Deep Analytics',
                        'description': 'Machine Learning Insights für Produktivität',
                        'example': 'deep analytics',
                        'expected_result': 'ML-basierte Produktivitäts-Patterns'
                    },
                    {
                        'step': 3,
                        'title': 'Wellness Integration',
                        'description': 'Starte eine Meditation oder Atemübung',
                        'example': 'start meditation',
                        'expected_result': 'Geführte Meditation-Session'
                    }
                ]
            },
            
            'developer_features': {
                'title': '🔧 Entwickler-Features',
                'description': 'Git-Integration und Automatisierung',
                'steps': [
                    {
                        'step': 1,
                        'title': 'Git-Repository Scan',
                        'description': 'Scanne alle Git-Repositories',
                        'example': 'git scan',
                        'expected_result': 'Repository-Dashboard mit Gesundheits-Status'
                    },
                    {
                        'step': 2,
                        'title': 'Bulk Git-Operationen',
                        'description': 'Führe Git-Befehle auf allen Repos aus',
                        'example': 'git pull all',
                        'expected_result': 'Bulk-Operation Ergebnis'
                    },
                    {
                        'step': 3,
                        'title': 'Automatisierungs-Regeln',
                        'description': 'Erstelle intelligente Automatisierung',
                        'example': 'create daily backup rule',
                        'expected_result': 'Automatisierungs-Regel erstellt'
                    }
                ]
            }
        }
        
        self.tutorials.update(tutorials)
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Liefert komplette System-Übersicht"""
        overview = {
            'system_info': {
                'name': 'Toobix AI Assistant',
                'version': '3.0 - Phase 3 Enhanced',
                'description': 'Revolutionäres KI-Productivity-Ecosystem',
                'total_components': len(self.system_components),
                'total_functions': len(self.function_docs),
                'last_updated': datetime.now().isoformat()
            },
            'components': {
                name: asdict(component) 
                for name, component in self.system_components.items()
            },
            'categories': self._get_function_categories(),
            'quick_stats': self._get_quick_stats()
        }
        
        return overview
    
    def get_function_documentation(self, category: str = None) -> Dict[str, Any]:
        """Liefert Funktions-Dokumentation"""
        if category:
            filtered_functions = {
                name: func for name, func in self.function_docs.items()
                if func.category.lower() == category.lower()
            }
        else:
            filtered_functions = self.function_docs
        
        return {
            'functions': {name: asdict(func) for name, func in filtered_functions.items()},
            'categories': self._get_function_categories(),
            'total_functions': len(filtered_functions)
        }
    
    def get_tutorial(self, tutorial_name: str) -> Dict[str, Any]:
        """Liefert spezifisches Tutorial"""
        if tutorial_name not in self.tutorials:
            return {'error': f'Tutorial "{tutorial_name}" nicht gefunden'}
        
        return {
            'tutorial': self.tutorials[tutorial_name],
            'available_tutorials': list(self.tutorials.keys())
        }
    
    def get_all_tutorials(self) -> Dict[str, Any]:
        """Liefert alle verfügbaren Tutorials"""
        return {
            'tutorials': self.tutorials,
            'tutorial_count': len(self.tutorials)
        }
    
    def search_functions(self, query: str) -> Dict[str, Any]:
        """Sucht Funktionen basierend auf Query"""
        query_lower = query.lower()
        matching_functions = {}
        
        for name, func in self.function_docs.items():
            if (query_lower in name.lower() or 
                query_lower in func.description.lower() or
                query_lower in func.category.lower() or
                any(query_lower in example.lower() for example in func.examples)):
                matching_functions[name] = func
        
        return {
            'query': query,
            'matches': {name: asdict(func) for name, func in matching_functions.items()},
            'match_count': len(matching_functions)
        }
    
    def _get_function_categories(self) -> Dict[str, int]:
        """Ermittelt Funktions-Kategorien und Anzahl"""
        categories = {}
        for func in self.function_docs.values():
            categories[func.category] = categories.get(func.category, 0) + 1
        return categories
    
    def _get_quick_stats(self) -> Dict[str, Any]:
        """Ermittelt Quick-Stats"""
        active_components = sum(1 for comp in self.system_components.values() if comp.status == 'active')
        working_functions = sum(1 for func in self.function_docs.values() if func.status == 'working')
        
        return {
            'active_components': active_components,
            'total_components': len(self.system_components),
            'working_functions': working_functions,
            'total_functions': len(self.function_docs),
            'system_health': 'Excellent' if active_components == len(self.system_components) else 'Good'
        }
    
    def get_component_details(self, component_name: str) -> Dict[str, Any]:
        """Liefert detaillierte Komponenten-Info"""
        if component_name not in self.system_components:
            return {'error': f'Komponente "{component_name}" nicht gefunden'}
        
        component = self.system_components[component_name]
        return {
            'component': asdict(component),
            'related_functions': self._get_related_functions(component_name)
        }
    
    def _get_related_functions(self, component_name: str) -> List[str]:
        """Findet verwandte Funktionen für Komponente"""
        related = []
        component_keywords = component_name.lower().split('_')
        
        for func_name, func in self.function_docs.items():
            if any(keyword in func.description.lower() or 
                   keyword in func.category.lower() 
                   for keyword in component_keywords):
                related.append(func_name)
        
        return related
    
    def get_system_architecture(self) -> Dict[str, Any]:
        """Liefert System-Architektur-Übersicht"""
        architecture = {
            'layers': {
                'presentation': {
                    'description': 'GUI und User Interface',
                    'components': ['main_window', 'chat_interface', 'speech_interface']
                },
                'application': {
                    'description': 'Core Application Logic',
                    'components': ['ai_handler', 'context_manager', 'gamification']
                },
                'intelligence': {
                    'description': 'KI und Analytics Engine',
                    'components': ['analytics_engine', 'wellness_engine', 'ollama', 'groq']
                },
                'system': {
                    'description': 'System Integration',
                    'components': ['system_monitor', 'git_integration', 'task_scheduler']
                },
                'data': {
                    'description': 'Data Storage und Persistence',
                    'components': ['json_storage', 'analytics_data', 'user_preferences']
                }
            },
            'data_flow': [
                'User Input → GUI → AI Handler',
                'AI Handler → Ollama/Groq → Response',
                'Context Manager → Analytics Engine → Insights',
                'Wellness Engine → Biofeedback → Recommendations',
                'All Components → Data Layer → Persistence'
            ],
            'integration_points': {
                'speech_recognition': 'Kontinuierliche Voice Input',
                'system_monitoring': 'Real-time Performance Data',
                'git_integration': 'Development Workflow',
                'wellness_tracking': 'Holistic User Experience'
            }
        }
        
        return architecture

if __name__ == "__main__":
    # Test der Documentation Engine
    doc_engine = SystemDocumentationEngine()
    
    # System Overview
    overview = doc_engine.get_system_overview()
    print("System Overview:", json.dumps(overview, indent=2, default=str))
    
    # Function Search
    search_result = doc_engine.search_functions("git")
    print("Git Functions:", json.dumps(search_result, indent=2, default=str))
