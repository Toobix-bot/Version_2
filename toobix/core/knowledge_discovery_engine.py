"""
Knowledge Discovery Center - Phase 5.2
Interaktive Wissensbasis zum Durchklicken und Erkunden
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class KnowledgeItem:
    """Einzelnes Wissenselement"""
    id: str
    title: str
    description: str
    category: str
    tags: List[str]
    content: str
    examples: List[str]
    related_items: List[str]
    difficulty_level: str  # 'beginner', 'intermediate', 'advanced'
    last_updated: str
    usage_count: int = 0
    user_rating: float = 0.0

@dataclass
class KnowledgeCategory:
    """Wissens-Kategorie"""
    id: str
    name: str
    description: str
    icon: str
    items: List[KnowledgeItem]
    subcategories: List[str] = None

@dataclass
class LearningPath:
    """Strukturierter Lernpfad"""
    id: str
    title: str
    description: str
    steps: List[str]  # Knowledge Item IDs
    estimated_time: int  # Minuten
    prerequisites: List[str]
    completion_rate: float = 0.0

class KnowledgeDiscoveryEngine:
    """
    Hauptengine für das Knowledge Discovery Center
    Verwaltet alle Wissensinhalte und Navigationswege
    """
    
    def __init__(self):
        self.knowledge_base = {}
        self.categories = {}
        self.learning_paths = {}
        self.user_progress = {}
        self.search_index = {}
        
        # Initialize with base knowledge
        self._initialize_knowledge_base()
        self._build_search_index()
        
        logger.info("📚 Knowledge Discovery Engine initialisiert")
    
    def _initialize_knowledge_base(self):
        """Initialisiert die Basis-Wissensbasis"""
        
        # === SYSTEM FEATURES ===
        system_items = [
            KnowledgeItem(
                id="system_monitoring",
                title="System-Überwachung",
                description="Echtzeitüberwachung von CPU, Memory, Disk und Netzwerk",
                category="system",
                tags=["monitoring", "performance", "hardware"],
                content="""
🖥️ SYSTEM-ÜBERWACHUNG

Die System-Überwachung bietet dir vollständige Transparenz über deinen Computer:

📊 ÜBERWACHTE METRIKEN:
• CPU-Auslastung (in Echtzeit)
• Arbeitsspeicher-Nutzung
• Festplatten-Speicher und I/O
• Netzwerk-Traffic
• Laufende Prozesse
• System-Temperatur (falls verfügbar)

🚀 AUTOMATISCHE OPTIMIERUNG:
• Erkennt Performance-Probleme
• Schlägt Optimierungen vor
• Kann automatisch aufräumen
• Überwacht kritische Schwellwerte

💡 PROAKTIVE WARNUNGEN:
• CPU über 90% für >5 Minuten
• Memory über 85%
• Festplatte über 90% voll
• Ungewöhnliche Netzwerkaktivität
                """,
                examples=[
                    "Sage: 'System-Status' um aktuellen Zustand zu sehen",
                    "Sage: 'Performance optimieren' für automatische Verbesserungen",
                    "Sage: 'Erweiterte Überwachung' für detaillierte Analyse"
                ],
                related_items=["task_manager", "performance_optimization"],
                difficulty_level="beginner",
                last_updated=datetime.now().isoformat()
            ),
            
            KnowledgeItem(
                id="task_management",
                title="Intelligenter Task-Manager",
                description="KI-gestützter Task-Scheduler mit automatischer Priorisierung",
                category="productivity",
                tags=["tasks", "scheduling", "automation"],
                content="""
⏰ INTELLIGENTER TASK-MANAGER

Der KI-Task-Manager hilft dir beim Organisieren und Priorisieren:

🎯 FEATURES:
• Automatische Priorisierung basierend auf Deadlines
• Kontextbasierte Erinnerungen
• Energie-Level Berücksichtigung
• Produktivitäts-Pattern Analyse

📅 SMART SCHEDULING:
• Optimale Zeiten für verschiedene Aufgaben
• Berücksichtigung deines Biorhythmus
• Automatic Rescheduling bei Verzögerungen
• Integration mit Kalender-Apps

🤖 KI-UNTERSTÜTZUNG:
• Schätzt Aufgabendauer automatisch
• Erkennt ähnliche Aufgaben
• Schlägt Batch-Processing vor
• Lernt aus deinen Gewohnheiten
                """,
                examples=[
                    "Sage: 'Erstelle Task: Präsentation vorbereiten bis Freitag'",
                    "Sage: 'Zeige heutige Aufgaben'",
                    "Sage: 'Optimiere meinen Tagesplan'"
                ],
                related_items=["time_management", "productivity_tracking"],
                difficulty_level="intermediate",
                last_updated=datetime.now().isoformat()
            ),
            
            KnowledgeItem(
                id="file_organization",
                title="Automatische Datei-Organisation",
                description="KI-basierte Sortierung und Strukturierung von Dateien",
                category="organization",
                tags=["files", "automation", "organization"],
                content="""
🗂️ AUTOMATISCHE DATEI-ORGANISATION

Toobix kann deine Dateien intelligent organisieren:

📁 SMART KATEGORISIERUNG:
• Erkennt Dateitypen automatisch
• Sortiert nach Inhalt und Kontext
• Erstellt logische Ordnerstrukturen
• Berücksichtigt deine Arbeitsweise

🔍 ERWEITERTE ERKENNUNG:
• Duplikat-Finder mit intelligenter Analyse
• Inhaltsbasierte Gruppierung
• Projekt-bezogene Sortierung
• Temporal Clustering (nach Erstellungsdatum)

⚡ BATCH-OPERATIONEN:
• Organisiert komplette Verzeichnisse
• Sichere Vorschau vor Änderungen
• Undo-Funktionalität
• Backup vor Reorganisation

🎯 ANPASSBARE REGELN:
• Eigene Kategorien definieren
• Ausnahme-Regeln erstellen
• Workflow-basierte Sortierung
• Lern-Algorithmus für Präferenzen
                """,
                examples=[
                    "Sage: 'Organisiere meinen Desktop'",
                    "Sage: 'Sortiere Downloads nach Kategorien'",
                    "Sage: 'Finde Duplikate in Dokumenten'"
                ],
                related_items=["backup_management", "cleanup_tools"],
                difficulty_level="beginner",
                last_updated=datetime.now().isoformat()
            )
        ]
        
        # === AI & INTELLIGENCE ===
        ai_items = [
            KnowledgeItem(
                id="hybrid_ai_system",
                title="Hybrid AI System",
                description="Kombination aus lokaler Ollama-KI und Cloud-Groq für optimale Performance",
                category="ai",
                tags=["ollama", "groq", "hybrid", "ai"],
                content="""
🧠 HYBRID AI SYSTEM

Toobix nutzt das Beste aus beiden Welten:

🏠 LOKALE KI (OLLAMA):
• Gemma 3:1b Model für schnelle Antworten
• Komplett offline und privat
• Keine Datenübertragung ins Internet
• Optimiert für alltägliche Aufgaben

☁️ CLOUD KI (GROQ):
• Hochleistungs-Modelle für komplexe Anfragen
• Fallback wenn lokale KI überlastet
• Spezialisiert auf schwierige Probleme
• Ultra-schnelle Inferenz

🔄 INTELLIGENTE UMSCHALTUNG:
• Automatische Lastverteilung
• Kontext-bewusste Modell-Auswahl
• Failover-Mechanismen
• Performance-Optimierung

🛡️ PRIVACY-FIRST:
• Lokale KI als Standard
• Cloud nur bei Bedarf
• Keine sensiblen Daten in der Cloud
• Vollständige Kontrolle über Daten
                """,
                examples=[
                    "Einfache Fragen → Lokale Ollama KI",
                    "Komplexe Analysen → Cloud Groq KI",
                    "System automatisch entscheidet optimal"
                ],
                related_items=["privacy_settings", "performance_tuning"],
                difficulty_level="advanced",
                last_updated=datetime.now().isoformat()
            ),
            
            KnowledgeItem(
                id="thought_stream",
                title="KI Gedankenstrom",
                description="Kontinuierlicher Stream von KI-Gedanken und Einsichten",
                category="ai",
                tags=["thoughts", "insights", "continuous"],
                content="""
🌊 KI GEDANKENSTROM

Die KI denkt kontinuierlich mit und teilt Einsichten:

💭 GEDANKEN-TYPEN:
• Insights: Wichtige Erkenntnisse
• Suggestions: Handlungsvorschläge  
• Observations: Interessante Beobachtungen
• Questions: Klärende Nachfragen
• Connections: Verbindungen zwischen Themen

🎯 INTELLIGENTE FILTERUNG:
• Nur relevante Gedanken werden gezeigt
• Prioritäts-basierte Auswahl
• Kontext-sensitive Insights
• Lernender Relevanz-Filter

⚡ ECHTZEIT-VERARBEITUNG:
• Kontinuierliche Hintergrund-Analyse
• Proaktive Problemerkennung
• Mustererkennung in deinem Verhalten
• Automatische Optimierungsvorschläge

🔗 INTEGRATION:
• Gedanken werden zu Chat-Nachrichten
• Verbindung zu Smart Suggestions
• Einfluss auf System-Entscheidungen
• Personalisierte KI-Persönlichkeit
                """,
                examples=[
                    "Gedanke: 'Du arbeitest schon 2h - vielleicht eine Pause?'",
                    "Insight: 'Pattern erkannt: Du bist vormittags produktiver'",
                    "Suggestion: 'Ähnliche Dateien in Projekt X gefunden'"
                ],
                related_items=["ai_personality", "productivity_insights"],
                difficulty_level="intermediate",
                last_updated=datetime.now().isoformat()
            )
        ]
        
        # === WELLNESS & LIFESTYLE ===
        wellness_items = [
            KnowledgeItem(
                id="wellness_engine",
                title="Creative Wellness Engine",
                description="Ganzheitliches Wellness-System mit Meditation, Atemübungen und Soundscapes",
                category="wellness",
                tags=["meditation", "breathing", "soundscapes", "health"],
                content="""
🎵 CREATIVE WELLNESS ENGINE

Dein persönlicher Wellness-Begleiter für Work-Life-Balance:

🧘 MEDITATION & ACHTSAMKEIT:
• Geführte Meditationen (5/10/15 Min)
• Verschiedene Stile: Calm, Focus, Sleep
• Binaural Beats für tiefere Entspannung
• Fortschritts-Tracking und Statistiken

🫁 ATEMÜBUNGEN:
• 4-7-8 Breathing für Entspannung
• Box Breathing für Fokus
• Energizing Breath für Aktivierung
• Adaptive Guidance basierend auf Stress-Level

🎼 ADAPTIVE SOUNDSCAPES:
• Konzentrations-Sounds (Focus Mode)
• Kreativitäts-Soundscapes
• Entspannungs-Ambient
• Natur-Sounds mit räumlichem Audio

📊 WELLNESS-MONITORING:
• Stress-Level Detection
• Energy-Pattern Tracking
• Produktivitäts-Korrelation
• Automatische Pausen-Empfehlungen
                """,
                examples=[
                    "Sage: 'Starte 5-Minuten Meditation'",
                    "Sage: 'Beginne Atemübung'",
                    "Sage: 'Spiele Focus-Soundscape ab'"
                ],
                related_items=["stress_management", "productivity_optimization"],
                difficulty_level="beginner",
                last_updated=datetime.now().isoformat()
            )
        ]
        
        # === AUTOMATION & SCRIPTING ===
        automation_items = [
            KnowledgeItem(
                id="smart_automation",
                title="Smart Automation Framework",
                description="Intelligente Automatisierung von wiederkehrenden Aufgaben",
                category="automation",
                tags=["automation", "scripts", "workflows"],
                content="""
🤖 SMART AUTOMATION FRAMEWORK

Automatisiere repetitive Aufgaben intelligent:

⚡ AUTO-ERKENNUNG:
• Identifiziert wiederholende Muster
• Schlägt Automatisierung vor
• Lernt aus deinem Verhalten
• Erstellt Custom Workflows

🔧 WORKFLOW-BUILDER:
• Drag & Drop Interface
• Trigger-basierte Aktionen
• Conditional Logic
• Multi-Step Sequences

📅 SCHEDULING:
• Zeitbasierte Ausführung
• Event-getriggerte Aktionen
• Kontext-sensitive Aktivierung
• Smart Retry-Mechanismen

🎯 BEISPIEL-AUTOMATISIERUNGEN:
• Täglich Desktop aufräumen
• Backup bei System-Shutdown
• Notifications bei wichtigen Events
• Automatic System Optimization
                """,
                examples=[
                    "Sage: 'Automatisiere meine Morgenroutine'",
                    "Sage: 'Erstelle Backup-Schedule'",
                    "Sage: 'Setup Smart Notifications'"
                ],
                related_items=["task_scheduling", "system_optimization"],
                difficulty_level="advanced",
                last_updated=datetime.now().isoformat()
            )
        ]
        
        # Speichere alle Items
        all_items = system_items + ai_items + wellness_items + automation_items
        for item in all_items:
            self.knowledge_base[item.id] = item
        
        # Erstelle Kategorien
        self.categories = {
            "system": KnowledgeCategory(
                id="system",
                name="System & Performance",
                description="Alles rund um System-Monitoring, Performance und Hardware",
                icon="🖥️",
                items=[item for item in all_items if item.category == "system"]
            ),
            "ai": KnowledgeCategory(
                id="ai",
                name="Künstliche Intelligenz",
                description="KI-Features, Modelle und intelligente Funktionen",
                icon="🧠",
                items=[item for item in all_items if item.category == "ai"]
            ),
            "productivity": KnowledgeCategory(
                id="productivity",
                name="Produktivität",
                description="Tools und Features für bessere Produktivität",
                icon="🎯",
                items=[item for item in all_items if item.category == "productivity"]
            ),
            "wellness": KnowledgeCategory(
                id="wellness",
                name="Wellness & Gesundheit",
                description="Features für Work-Life-Balance und Wohlbefinden",
                icon="🎵",
                items=[item for item in all_items if item.category == "wellness"]
            ),
            "automation": KnowledgeCategory(
                id="automation",
                name="Automatisierung",
                description="Workflows, Scripts und automatisierte Prozesse",
                icon="🤖",
                items=[item for item in all_items if item.category == "automation"]
            ),
            "organization": KnowledgeCategory(
                id="organization",
                name="Organisation",
                description="Datei-Management und strukturierte Organisation",
                icon="🗂️",
                items=[item for item in all_items if item.category == "organization"]
            )
        }
        
        # Erstelle Learning Paths
        self._create_learning_paths()
    
    def _create_learning_paths(self):
        """Erstellt strukturierte Lernpfade"""
        self.learning_paths = {
            "beginner_path": LearningPath(
                id="beginner_path",
                title="Toobix Grundlagen",
                description="Perfekter Einstieg in alle Toobix-Features",
                steps=[
                    "system_monitoring",
                    "file_organization", 
                    "wellness_engine",
                    "hybrid_ai_system"
                ],
                estimated_time=30,
                prerequisites=[]
            ),
            
            "productivity_master": LearningPath(
                id="productivity_master",
                title="Produktivitäts-Master",
                description="Werde zum Produktivitäts-Ninja mit Toobix",
                steps=[
                    "task_management",
                    "smart_automation",
                    "file_organization",
                    "thought_stream"
                ],
                estimated_time=45,
                prerequisites=["beginner_path"]
            ),
            
            "ai_expert": LearningPath(
                id="ai_expert",
                title="KI-Experte",
                description="Meistere alle KI-Features und verstehe das System",
                steps=[
                    "hybrid_ai_system",
                    "thought_stream", 
                    "smart_automation"
                ],
                estimated_time=35,
                prerequisites=["beginner_path"]
            )
        }
    
    def _build_search_index(self):
        """Erstellt Suchindex für schnelle Suche"""
        self.search_index = {}
        
        for item_id, item in self.knowledge_base.items():
            # Index für Titel, Beschreibung, Tags, Content
            searchable_text = f"{item.title} {item.description} {' '.join(item.tags)} {item.content}".lower()
            
            words = searchable_text.split()
            for word in words:
                if len(word) > 2:  # Ignoriere sehr kurze Wörter
                    if word not in self.search_index:
                        self.search_index[word] = []
                    if item_id not in self.search_index[word]:
                        self.search_index[word].append(item_id)
    
    def search(self, query: str, max_results: int = 10) -> List[KnowledgeItem]:
        """Sucht in der Wissensbasis"""
        query_words = query.lower().split()
        item_scores = {}
        
        for word in query_words:
            if word in self.search_index:
                for item_id in self.search_index[word]:
                    if item_id not in item_scores:
                        item_scores[item_id] = 0
                    item_scores[item_id] += 1
        
        # Sortiere nach Relevanz
        sorted_items = sorted(item_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for item_id, score in sorted_items[:max_results]:
            item = self.knowledge_base[item_id]
            results.append(item)
        
        return results
    
    def get_category(self, category_id: str) -> Optional[KnowledgeCategory]:
        """Gibt Kategorie zurück"""
        return self.categories.get(category_id)
    
    def get_all_categories(self) -> List[KnowledgeCategory]:
        """Gibt alle Kategorien zurück"""
        return list(self.categories.values())
    
    def get_item(self, item_id: str) -> Optional[KnowledgeItem]:
        """Gibt spezifisches Wissenselement zurück"""
        return self.knowledge_base.get(item_id)
    
    def get_related_items(self, item_id: str) -> List[KnowledgeItem]:
        """Gibt verwandte Elemente zurück"""
        item = self.get_item(item_id)
        if not item:
            return []
        
        related = []
        for related_id in item.related_items:
            related_item = self.get_item(related_id)
            if related_item:
                related.append(related_item)
        
        return related
    
    def get_learning_path(self, path_id: str) -> Optional[LearningPath]:
        """Gibt Lernpfad zurück"""
        return self.learning_paths.get(path_id)
    
    def get_all_learning_paths(self) -> List[LearningPath]:
        """Gibt alle Lernpfade zurück"""
        return list(self.learning_paths.values())
    
    def track_usage(self, item_id: str):
        """Trackt Nutzung eines Elements"""
        if item_id in self.knowledge_base:
            self.knowledge_base[item_id].usage_count += 1
    
    def rate_item(self, item_id: str, rating: float):
        """Bewertet ein Wissenselement"""
        if item_id in self.knowledge_base and 0 <= rating <= 5:
            item = self.knowledge_base[item_id]
            # Einfacher Durchschnitt (könnte erweitert werden)
            current_rating = item.user_rating
            item.user_rating = (current_rating + rating) / 2
    
    def get_popular_items(self, limit: int = 5) -> List[KnowledgeItem]:
        """Gibt beliebte Elemente basierend auf Nutzung zurück"""
        sorted_items = sorted(
            self.knowledge_base.values(),
            key=lambda x: x.usage_count,
            reverse=True
        )
        return sorted_items[:limit]
    
    def get_recommendations(self, based_on_item: str = None, user_interests: List[str] = None) -> List[KnowledgeItem]:
        """Gibt personalisierte Empfehlungen zurück"""
        recommendations = []
        
        if based_on_item:
            # Empfehlungen basierend auf ähnlichen Tags
            base_item = self.get_item(based_on_item)
            if base_item:
                for item in self.knowledge_base.values():
                    if item.id != based_on_item:
                        # Berechne Tag-Überlappung
                        common_tags = set(base_item.tags) & set(item.tags)
                        if len(common_tags) >= 2:  # Mindestens 2 gemeinsame Tags
                            recommendations.append(item)
        
        elif user_interests:
            # Empfehlungen basierend auf Interessen
            for item in self.knowledge_base.values():
                for interest in user_interests:
                    if interest.lower() in [tag.lower() for tag in item.tags]:
                        if item not in recommendations:
                            recommendations.append(item)
        
        else:
            # Fallback: Beliebte Items
            recommendations = self.get_popular_items()
        
        return recommendations[:5]
    
    def export_knowledge_summary(self) -> Dict[str, Any]:
        """Exportiert Zusammenfassung der Wissensbasis"""
        return {
            "total_items": len(self.knowledge_base),
            "categories": len(self.categories),
            "learning_paths": len(self.learning_paths),
            "categories_overview": {
                cat_id: {
                    "name": cat.name,
                    "item_count": len(cat.items),
                    "description": cat.description
                }
                for cat_id, cat in self.categories.items()
            },
            "popular_items": [
                {"id": item.id, "title": item.title, "usage": item.usage_count}
                for item in self.get_popular_items()
            ],
            "last_updated": datetime.now().isoformat()
        }
