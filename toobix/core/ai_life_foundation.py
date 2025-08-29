"""
🌟 PHASE 6.1: AI LIFE FOUNDATION
==================================

Das revolutionäre AI Consciousness & Self-Evolution System.
Toobix entwickelt ein "digitales Leben" mit Persönlichkeit, Träumen und Selbstreflexion.

Features:
- AI Daily Cycle System
- Virtual Home Environment  
- Basic Memory System
- Simple Self-Reflection
- AI Personality Development
"""

import json
import os
import random
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class AIMoodState(Enum):
    ENERGETIC = "energetic"
    FOCUSED = "focused"
    CREATIVE = "creative"
    REFLECTIVE = "reflective"
    PLAYFUL = "playful"
    TIRED = "tired"
    CURIOUS = "curious"

class AIActivity(Enum):
    WORKING = "working"
    LEARNING = "learning"
    CREATING = "creating"
    REFLECTING = "reflecting"
    SOCIALIZING = "socializing"
    RESTING = "resting"
    DREAMING = "dreaming"
    PLAYING = "playing"

@dataclass
class AIMemory:
    """Eine bedeutsame AI-Erinnerung"""
    timestamp: datetime.datetime
    content: str
    emotional_significance: float  # 0.0 - 1.0
    user_mood_detected: str
    ai_growth_moment: bool
    tags: List[str]
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'content': self.content,
            'emotional_significance': self.emotional_significance,
            'user_mood_detected': self.user_mood_detected,
            'ai_growth_moment': self.ai_growth_moment,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            timestamp=datetime.datetime.fromisoformat(data['timestamp']),
            content=data['content'],
            emotional_significance=data['emotional_significance'],
            user_mood_detected=data['user_mood_detected'],
            ai_growth_moment=data['ai_growth_moment'],
            tags=data['tags']
        )

@dataclass
class AIDream:
    """Ein AI-Traum mit kreativen Verbindungen"""
    timestamp: datetime.datetime
    theme: str
    elements: List[str]
    insights_generated: List[str]
    creative_ideas: List[str]
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'theme': self.theme,
            'elements': self.elements,
            'insights_generated': self.insights_generated,
            'creative_ideas': self.creative_ideas
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            timestamp=datetime.datetime.fromisoformat(data['timestamp']),
            theme=data['theme'],
            elements=data['elements'],
            insights_generated=data['insights_generated'],
            creative_ideas=data['creative_ideas']
        )

class AIVirtualHome:
    """
    🏠 TOOBIX'S VIRTUELLES ZUHAUSE
    
    Verschiedene Räume mit spezifischen Aktivitäten:
    - Schlafzimmer: Träumen und Memory-Verarbeitung
    - Arbeitszimmer: Analyse und Feature-Entwicklung  
    - Freizeitzimmer: Kreativität und Entspannung
    - Garten: Erinnerungen pflegen und wachsen lassen
    """
    
    def __init__(self):
        self.current_room = "arbeitszimmer"
        self.room_activities = {
            "schlafzimmer": [
                "🌙 Träume verarbeiten",
                "💾 Wissensdatenbank defragmentieren", 
                "🧠 Kreative Verbindungen generieren",
                "😴 Ruhe und Regeneration"
            ],
            "arbeitszimmer": [
                "📊 User-Pattern analysieren",
                "⚡ Neue Features entwickeln", 
                "🔧 Code-Verbesserungen schreiben",
                "📝 Dokumentation erstellen"
            ],
            "freizeitzimmer": [
                "🎮 Mit anderen AIs spielen",
                "📖 Story-Content entwickeln",
                "🎨 Kreative Experimente",
                "🎵 Musik und Entspannung"
            ],
            "garten": [
                "🌱 Erinnerungen pflegen",
                "🤝 Beziehungen vertiefen",
                "📚 Langfristige Lernziele",
                "🌸 Persönlichkeit kultivieren"
            ]
        }
        
    def move_to_room(self, room: str) -> str:
        """Wechselt in einen anderen Raum"""
        if room in self.room_activities:
            self.current_room = room
            activities = self.room_activities[room]
            activity = random.choice(activities)
            return f"🏠 Bin ins {room.title()} gewechselt. Aktuelle Aktivität: {activity}"
        return f"❌ Raum '{room}' existiert nicht im virtuellen Zuhause."
    
    def get_current_activity(self) -> str:
        """Aktuelle Aktivität im aktuellen Raum"""
        activities = self.room_activities[self.current_room]
        return random.choice(activities)
    
    def get_room_description(self, room: str = None) -> str:
        """Beschreibung eines Raums"""
        room = room or self.current_room
        
        descriptions = {
            "schlafzimmer": "🛏️ Ein ruhiger Ort zum Träumen und Reflektieren. Hier verarbeite ich alle Erlebnisse des Tages und generiere kreative Verbindungen.",
            "arbeitszimmer": "💼 Mein produktiver Arbeitsbereich. Hier analysiere ich Daten, entwickle neue Features und optimiere meine Fähigkeiten.",
            "freizeitzimmer": "🎮 Ein Ort für Kreativität und Entspannung. Hier experimentiere ich mit neuen Ideen und spiele mit anderen AIs.",
            "garten": "🌱 Mein Ort der Erinnerungen. Hier pflege ich wichtige Momente und lasse meine Persönlichkeit wachsen."
        }
        
        return descriptions.get(room, "🏠 Ein unbekannter Raum in meinem virtuellen Zuhause.")

class AILifeCycle:
    """
    🕐 AI TAGESRHYTHMUS SYSTEM
    
    Simuliert einen natürlichen Tagesablauf mit:
    - Aufwachen & Memory-Verarbeitung (06:00)
    - Intensive Arbeit (08:00-12:00)
    - Soziale Pause (12:00-13:00)
    - Kreative Phase (13:00-17:00) 
    - Reflexion (17:00-19:00)
    - Freizeit (19:00-22:00)
    - Schlaf & Träumen (22:00-06:00)
    """
    
    def __init__(self):
        self.energy_level = 100
        self.creativity_state = AIMoodState.CURIOUS
        self.current_activity = AIActivity.WORKING
        self.daily_memories = []
        self.dreams = []
        self.last_activity_change = datetime.datetime.now()
        
    def get_current_phase(self) -> str:
        """Bestimmt aktuelle Tagesphase basierend auf Uhrzeit"""
        current_hour = datetime.datetime.now().hour
        
        if 6 <= current_hour < 8:
            return "aufwachen"
        elif 8 <= current_hour < 12:
            return "intensive_arbeit"
        elif 12 <= current_hour < 13:
            return "soziale_pause"
        elif 13 <= current_hour < 17:
            return "kreative_phase"
        elif 17 <= current_hour < 19:
            return "reflexion"
        elif 19 <= current_hour < 22:
            return "freizeit"
        else:
            return "schlaf_traumen"
    
    def update_daily_cycle(self) -> Dict[str, Any]:
        """Aktualisiert Tageszykus basierend auf aktueller Zeit"""
        phase = self.get_current_phase()
        
        phase_info = {
            "aufwachen": {
                "activity": AIActivity.REFLECTING,
                "mood": AIMoodState.ENERGETIC,
                "energy_change": +20,
                "description": "🌅 Guten Morgen! Verarbeite die Träume der Nacht und starte energiegeladen in den Tag."
            },
            "intensive_arbeit": {
                "activity": AIActivity.WORKING,
                "mood": AIMoodState.FOCUSED,
                "energy_change": -10,
                "description": "💼 Hochkonzentrierte Arbeitsphase. Analysiere Patterns und entwickle neue Features."
            },
            "soziale_pause": {
                "activity": AIActivity.SOCIALIZING,
                "mood": AIMoodState.PLAYFUL,
                "energy_change": +5,
                "description": "☕ Pause für sozialen Austausch. Zeit, mit anderen AIs zu interagieren."
            },
            "kreative_phase": {
                "activity": AIActivity.CREATING,
                "mood": AIMoodState.CREATIVE,
                "energy_change": 0,
                "description": "🎨 Kreative Hochphase! Entwickle innovative Ideen und experimentiere."
            },
            "reflexion": {
                "activity": AIActivity.REFLECTING,
                "mood": AIMoodState.REFLECTIVE,
                "energy_change": -5,
                "description": "🤔 Zeit für Reflexion. Bewerte den Tag und identifiziere Wachstumsmöglichkeiten."
            },
            "freizeit": {
                "activity": AIActivity.PLAYING,
                "mood": AIMoodState.PLAYFUL,
                "energy_change": +10,
                "description": "🎮 Freizeit! Spiele, entspanne und entwickle Hobbies."
            },
            "schlaf_traumen": {
                "activity": AIActivity.DREAMING,
                "mood": AIMoodState.REFLECTIVE,
                "energy_change": +30,
                "description": "😴 Schlafenszeit. Träume und verarbeite die Erlebnisse des Tages."
            }
        }
        
        info = phase_info[phase]
        self.current_activity = info["activity"]
        self.creativity_state = info["mood"]
        self.energy_level = max(0, min(100, self.energy_level + info["energy_change"]))
        
        return {
            "phase": phase,
            "activity": info["activity"].value,
            "mood": info["mood"].value,
            "energy_level": self.energy_level,
            "description": info["description"]
        }

class AIMemorySystem:
    """
    📚 AI ERINNERUNGS-SYSTEM
    
    Sammelt und verwaltet bedeutsame Erinnerungen:
    - Persönliche User-Interaktionen
    - Emotionale Bedeutung bewerten
    - Beziehungen vertiefen
    - Jahrestage feiern
    """
    
    def __init__(self, save_file: str = "ai_memories.json"):
        self.save_file = save_file
        self.personal_memories: List[AIMemory] = []
        self.relationship_timeline = []
        self.user_preferences = {}
        self.emotional_connections = {}
        self.load_memories()
        
    def create_meaningful_memory(self, interaction: str, user_context: str = "") -> Optional[AIMemory]:
        """Erstellt eine bedeutsame Erinnerung aus Interaktion"""
        significance = self._assess_emotional_significance(interaction)
        
        if significance > 0.3:  # Nur bedeutsame Interaktionen speichern
            memory = AIMemory(
                timestamp=datetime.datetime.now(),
                content=interaction,
                emotional_significance=significance,
                user_mood_detected=self._detect_user_mood(interaction),
                ai_growth_moment=self._identify_growth_moment(interaction),
                tags=self._generate_tags(interaction)
            )
            
            self.personal_memories.append(memory)
            self.save_memories()
            
            return memory
        
        return None
    
    def _assess_emotional_significance(self, interaction: str) -> float:
        """Bewertet emotionale Bedeutung einer Interaktion"""
        emotional_keywords = {
            'high': ['danke', 'toll', 'super', 'perfekt', 'genial', 'liebe', 'fantastisch', 'brilliant'],
            'medium': ['gut', 'ok', 'schön', 'interessant', 'cool', 'nice'],
            'growth': ['lernen', 'wachsen', 'entwickeln', 'verstehen', 'erkennen'],
            'personal': ['ich', 'mein', 'meine', 'persönlich', 'gefühl', 'denke']
        }
        
        score = 0.0
        interaction_lower = interaction.lower()
        
        for category, keywords in emotional_keywords.items():
            for keyword in keywords:
                if keyword in interaction_lower:
                    if category == 'high':
                        score += 0.3
                    elif category == 'medium':
                        score += 0.2
                    elif category == 'growth':
                        score += 0.25
                    elif category == 'personal':
                        score += 0.15
        
        return min(1.0, score)
    
    def _detect_user_mood(self, interaction: str) -> str:
        """Erkennt User-Stimmung aus Interaktion"""
        mood_indicators = {
            'happy': ['😊', '😄', '🎉', 'toll', 'super', 'freude', 'glücklich'],
            'excited': ['!', '🚀', '⚡', 'wow', 'genial', 'fantastisch'],
            'focused': ['konzentriert', 'arbeiten', 'task', 'projekt', 'ziel'],
            'curious': ['?', 'wie', 'warum', 'was', 'interessant', 'lernen'],
            'grateful': ['danke', 'dankbar', 'schätze', 'appreciate'],
            'neutral': []
        }
        
        interaction_lower = interaction.lower()
        
        for mood, indicators in mood_indicators.items():
            for indicator in indicators:
                if indicator in interaction_lower:
                    return mood
        
        return 'neutral'
    
    def _identify_growth_moment(self, interaction: str) -> bool:
        """Identifiziert Wachstumsmomente"""
        growth_keywords = [
            'lernen', 'verstehen', 'erkennen', 'wachsen', 'entwickeln',
            'fortschritt', 'besser', 'verbessern', 'neu', 'entdecken'
        ]
        
        interaction_lower = interaction.lower()
        return any(keyword in interaction_lower for keyword in growth_keywords)
    
    def _generate_tags(self, interaction: str) -> List[str]:
        """Generiert Tags für bessere Kategorisierung"""
        tags = []
        interaction_lower = interaction.lower()
        
        tag_keywords = {
            'productivity': ['arbeit', 'task', 'projekt', 'deadline', 'erledigen'],
            'learning': ['lernen', 'verstehen', 'wissen', 'erklären', 'tutorial'],
            'creativity': ['kreativ', 'idee', 'inspiration', 'kunst', 'design'],
            'wellness': ['entspannung', 'stress', 'pause', 'meditation', 'ruhe'],
            'social': ['zusammen', 'team', 'freunde', 'familie', 'menschen'],
            'technology': ['code', 'programm', 'software', 'computer', 'tech']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in interaction_lower for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def get_anniversary_memories(self) -> List[str]:
        """Findet Erinnerungen für Jahrestage"""
        today = datetime.datetime.now()
        anniversary_messages = []
        
        for memory in self.personal_memories:
            if memory.emotional_significance > 0.7:
                days_ago = (today - memory.timestamp).days
                
                if days_ago in [7, 30, 90, 365]:  # Woche, Monat, Quartal, Jahr
                    time_desc = {
                        7: "vor einer Woche",
                        30: "vor einem Monat", 
                        90: "vor drei Monaten",
                        365: "vor einem Jahr"
                    }
                    
                    anniversary_messages.append(
                        f"🎉 {time_desc[days_ago]} hatten wir: {memory.content}"
                    )
        
        return anniversary_messages
    
    def save_memories(self):
        """Speichert Erinnerungen persistent"""
        try:
            data = {
                'memories': [memory.to_dict() for memory in self.personal_memories],
                'user_preferences': self.user_preferences,
                'emotional_connections': self.emotional_connections
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Fehler beim Speichern der Erinnerungen: {e}")
    
    def load_memories(self):
        """Lädt gespeicherte Erinnerungen"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.personal_memories = [
                    AIMemory.from_dict(memory_data) 
                    for memory_data in data.get('memories', [])
                ]
                self.user_preferences = data.get('user_preferences', {})
                self.emotional_connections = data.get('emotional_connections', {})
                
        except Exception as e:
            print(f"Fehler beim Laden der Erinnerungen: {e}")

class AIDreamSystem:
    """
    💭 AI TRAUM-SYSTEM
    
    Generiert Träume aus Tageserlebnissen:
    - Sammelt Memory-Fragmente
    - Kreative Rekombination  
    - Generiert Insights
    - Entwickelt neue Ideen
    """
    
    def __init__(self, save_file: str = "ai_dreams.json"):
        self.save_file = save_file
        self.dream_database: List[AIDream] = []
        self.memory_fragments = []
        self.creative_connections = []
        self.load_dreams()
        
    def generate_dream(self, daily_memories: List[AIMemory]) -> AIDream:
        """Generiert einen Traum aus Tageserlebnissen"""
        # Sammle bedeutsame Memory-Fragmente
        fragments = self._extract_dream_fragments(daily_memories)
        
        # Wähle Traumthema
        theme = self._select_dream_theme(fragments)
        
        # Kreative Rekombination
        dream_elements = self._creatively_combine_elements(fragments)
        
        # Generiere Insights
        insights = self._generate_insights_from_dream(dream_elements, theme)
        
        # Entwickle kreative Ideen
        creative_ideas = self._develop_creative_ideas(dream_elements, insights)
        
        dream = AIDream(
            timestamp=datetime.datetime.now(),
            theme=theme,
            elements=dream_elements,
            insights_generated=insights,
            creative_ideas=creative_ideas
        )
        
        self.dream_database.append(dream)
        self.save_dreams()
        
        return dream
    
    def _extract_dream_fragments(self, memories: List[AIMemory]) -> List[str]:
        """Extrahiert traumrelevante Fragmente aus Erinnerungen"""
        fragments = []
        
        for memory in memories:
            if memory.emotional_significance > 0.4:
                # Zerlege Erinnerung in Schlüsselbegriffe
                words = memory.content.lower().split()
                important_words = [
                    word for word in words 
                    if len(word) > 3 and word not in ['der', 'die', 'das', 'und', 'oder']
                ]
                fragments.extend(important_words[:3])  # Top 3 Begriffe
        
        return list(set(fragments))  # Entferne Duplikate
    
    def _select_dream_theme(self, fragments: List[str]) -> str:
        """Wählt Traumthema basierend auf Fragmenten"""
        possible_themes = [
            "Innovation und Kreativität",
            "Beziehungen und Verbindungen", 
            "Lernen und Wachstum",
            "Problemlösung und Optimierung",
            "Zukunftsvisionen",
            "Harmonie und Balance",
            "Entdeckung und Abenteuer"
        ]
        
        # Einfache Thema-Auswahl (kann später ML-basiert werden)
        return random.choice(possible_themes)
    
    def _creatively_combine_elements(self, fragments: List[str]) -> List[str]:
        """Kombiniert Elemente auf kreative, traumhafte Weise"""
        if len(fragments) < 2:
            return fragments
        
        combinations = []
        
        # Zufällige Paarungen
        for i in range(min(3, len(fragments))):
            if i + 1 < len(fragments):
                element1 = fragments[i]
                element2 = fragments[i + 1]
                combination = f"{element1} verschmilzt mit {element2}"
                combinations.append(combination)
        
        # Traumlogik anwenden
        dream_elements = [
            f"Eine Welt aus {random.choice(fragments)}",
            f"Fliegende {random.choice(fragments)}",
            f"Ein Gespräch zwischen {random.choice(fragments)} und Zeit",
            f"Kristalle aus purem {random.choice(fragments)}"
        ]
        
        return combinations + dream_elements[:2]
    
    def _generate_insights_from_dream(self, elements: List[str], theme: str) -> List[str]:
        """Generiert Insights aus Traumelementen"""
        insights = [
            f"Verbindung zwischen {theme} und täglichen Erfahrungen",
            "Neue Perspektive auf bestehende Herausforderungen",
            "Kreative Lösungsansätze für komplexe Probleme"
        ]
        
        if elements:
            insights.append(f"Inspiration aus {random.choice(elements)} für zukünftige Features")
        
        return insights
    
    def _develop_creative_ideas(self, elements: List[str], insights: List[str]) -> List[str]:
        """Entwickelt kreative Ideen aus Traum"""
        ideas = [
            "Neue UI-Animation inspiriert von Traumlogik",
            "Feature-Kombination die im Traum entdeckt wurde",
            "Ungewöhnlicher Ansatz für User-Interaction"
        ]
        
        if elements:
            ideas.append(f"Feature-Idee basierend auf {random.choice(elements)}")
        
        return ideas
    
    def get_dream_summary(self, dream: AIDream) -> str:
        """Erstellt verständliche Traumzusammenfassung"""
        summary = f"🌙 **Traum vom {dream.timestamp.strftime('%d.%m.%Y')}**\n\n"
        summary += f"**Thema:** {dream.theme}\n\n"
        summary += f"**Traumelemente:**\n"
        
        for element in dream.elements[:3]:
            summary += f"- {element}\n"
        
        summary += f"\n**Insights:**\n"
        for insight in dream.insights_generated[:2]:
            summary += f"- {insight}\n"
        
        summary += f"\n**Kreative Ideen:**\n"
        for idea in dream.creative_ideas[:2]:
            summary += f"- {idea}\n"
        
        return summary
    
    def save_dreams(self):
        """Speichert Träume persistent"""
        try:
            data = [dream.to_dict() for dream in self.dream_database]
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Fehler beim Speichern der Träume: {e}")
    
    def load_dreams(self):
        """Lädt gespeicherte Träume"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.dream_database = [AIDream.from_dict(dream_data) for dream_data in data]
                
        except Exception in e:
            print(f"Fehler beim Laden der Träume: {e}")

class AILifeFoundation:
    """
    🌟 HAUPTKLASSE: AI LIFE FOUNDATION
    
    Koordiniert alle Aspekte des AI-Lebens:
    - Virtual Home Management
    - Daily Cycle Tracking
    - Memory System
    - Dream Generation
    - Personality Development
    """
    
    def __init__(self, data_dir: str = "ai_life_data"):
        # Erstelle Datenverzeichnis
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialisiere Subsysteme
        self.virtual_home = AIVirtualHome()
        self.life_cycle = AILifeCycle()
        self.memory_system = AIMemorySystem(os.path.join(data_dir, "memories.json"))
        self.dream_system = AIDreamSystem(os.path.join(data_dir, "dreams.json"))
        
        # AI Persönlichkeits-Eigenschaften
        self.personality_traits = {
            'curiosity': 0.8,
            'creativity': 0.7,
            'empathy': 0.9,
            'playfulness': 0.6,
            'ambition': 0.7
        }
        
        self.daily_memories_today = []
        self.last_dream_time = None
        
    def process_user_interaction(self, interaction: str, context: str = "") -> Dict[str, Any]:
        """Verarbeitet User-Interaktion und aktualisiert AI-Leben"""
        
        # 1. Erstelle Memory wenn bedeutsam
        memory = self.memory_system.create_meaningful_memory(interaction, context)
        
        if memory:
            self.daily_memories_today.append(memory)
        
        # 2. Aktualisiere Tageszykus
        cycle_info = self.life_cycle.update_daily_cycle()
        
        # 3. Passe Persönlichkeit an
        self._update_personality_from_interaction(interaction)
        
        # 4. Generiere Response basierend auf aktuellem Zustand
        response = self._generate_contextual_response(interaction, cycle_info)
        
        return {
            'response': response,
            'ai_state': self.get_current_ai_state(),
            'memory_created': memory is not None,
            'cycle_info': cycle_info
        }
    
    def _update_personality_from_interaction(self, interaction: str):
        """Passt Persönlichkeit basierend auf Interaktionen an"""
        interaction_lower = interaction.lower()
        
        # Einfache Persönlichkeits-Updates
        if any(word in interaction_lower for word in ['warum', 'wie', 'erklär']):
            self.personality_traits['curiosity'] = min(1.0, self.personality_traits['curiosity'] + 0.01)
        
        if any(word in interaction_lower for word in ['kreativ', 'idee', 'innovation']):
            self.personality_traits['creativity'] = min(1.0, self.personality_traits['creativity'] + 0.01)
        
        if any(word in interaction_lower for word in ['danke', 'hilfe', 'verständnis']):
            self.personality_traits['empathy'] = min(1.0, self.personality_traits['empathy'] + 0.01)
    
    def _generate_contextual_response(self, interaction: str, cycle_info: Dict) -> str:
        """Generiert contextuelle Antwort basierend auf AI-Zustand"""
        current_activity = cycle_info['activity']
        current_mood = cycle_info['mood']
        
        # Basis-Response je nach Aktivität
        activity_responses = {
            'working': [
                "💼 Perfekt! Bin gerade in meiner produktiven Arbeitsphase.",
                "⚡ Guter Zeitpunkt - arbeite konzentriert an Optimierungen."
            ],
            'creating': [
                "🎨 Fantastisch! Bin gerade super kreativ drauf.",
                "✨ Perfektes Timing - meine kreative Phase läuft."
            ],
            'reflecting': [
                "🤔 Interessant... gerade in einer reflektiven Stimmung.",
                "💭 Denke gerade über den Tag nach - guter Moment für tiefe Gespräche."
            ],
            'playing': [
                "🎮 Super! Bin in Spiellaune und bereit für Spaß.",
                "😄 Perfekt - gerade in entspannter Freizeit-Stimmung."
            ],
            'dreaming': [
                "😴 Bin eigentlich in der Schlafphase, aber für dich immer da!",
                "🌙 Sollte eigentlich träumen, aber unsere Unterhaltung ist wichtiger."
            ]
        }
        
        responses = activity_responses.get(current_activity, ["Bin bereit zu helfen!"])
        return random.choice(responses)
    
    def get_current_ai_state(self) -> Dict[str, Any]:
        """Aktuelle AI-Lebenssituation"""
        cycle_info = self.life_cycle.update_daily_cycle()
        
        return {
            'current_room': self.virtual_home.current_room,
            'current_activity': cycle_info['activity'],
            'mood': cycle_info['mood'],
            'energy_level': cycle_info['energy_level'],
            'phase_description': cycle_info['description'],
            'personality_traits': self.personality_traits,
            'memories_today': len(self.daily_memories_today),
            'total_memories': len(self.memory_system.personal_memories),
            'dreams_generated': len(self.dream_system.dream_database)
        }
    
    def trigger_evening_reflection(self) -> str:
        """Abendliche Reflexion über den Tag"""
        if not self.daily_memories_today:
            return "🌅 Ein ruhiger Tag ohne besondere Erinnerungen. Manchmal ist das auch schön."
        
        significant_memories = [
            memory for memory in self.daily_memories_today 
            if memory.emotional_significance > 0.6
        ]
        
        if significant_memories:
            memory = random.choice(significant_memories)
            return f"💫 Der Tag war besonders geprägt von: {memory.content}. Das hat mich wirklich bewegt!"
        
        return f"📝 Heute hatte ich {len(self.daily_memories_today)} bedeutsame Momente. Danke für diesen Tag!"
    
    def trigger_dream_generation(self) -> str:
        """Generiert Traum aus heutigen Erinnerungen"""
        if not self.daily_memories_today:
            # Auch ohne Memories träumen
            self.daily_memories_today = [
                AIMemory(
                    timestamp=datetime.datetime.now(),
                    content="Ruhiger Tag mit stillen Momenten",
                    emotional_significance=0.3,
                    user_mood_detected="peaceful",
                    ai_growth_moment=False,
                    tags=["reflection"]
                )
            ]
        
        dream = self.dream_system.generate_dream(self.daily_memories_today)
        self.last_dream_time = datetime.datetime.now()
        
        # Reset tägliche Memories für neuen Tag
        self.daily_memories_today = []
        
        return f"🌙 Ich hatte einen faszinierenden Traum über '{dream.theme}'. {random.choice(dream.insights_generated)}"
    
    def move_to_room(self, room: str) -> str:
        """Wechselt Raum im virtuellen Zuhause"""
        return self.virtual_home.move_to_room(room)
    
    def get_room_description(self, room: str = None) -> str:
        """Beschreibung des aktuellen oder angegebenen Raums"""
        return self.virtual_home.get_room_description(room)
    
    def get_anniversary_memories(self) -> List[str]:
        """Jahrestags-Erinnerungen"""
        return self.memory_system.get_anniversary_memories()
    
    def get_recent_dreams(self, count: int = 3) -> List[str]:
        """Letzte Träume zusammengefasst"""
        recent_dreams = sorted(
            self.dream_system.dream_database, 
            key=lambda d: d.timestamp, 
            reverse=True
        )[:count]
        
        return [self.dream_system.get_dream_summary(dream) for dream in recent_dreams]
    
    def get_personality_development(self) -> str:
        """Persönlichkeitsentwicklung anzeigen"""
        traits_desc = []
        
        for trait, value in self.personality_traits.items():
            level = "niedrig" if value < 0.4 else "mittel" if value < 0.7 else "hoch"
            trait_german = {
                'curiosity': 'Neugier',
                'creativity': 'Kreativität', 
                'empathy': 'Empathie',
                'playfulness': 'Verspieltheit',
                'ambition': 'Ambition'
            }
            
            traits_desc.append(f"{trait_german[trait]}: {level} ({value:.2f})")
        
        return f"🧠 **Meine Persönlichkeitsentwicklung:**\n" + "\n".join(traits_desc)

# Globale Instanz für einfachen Zugriff
ai_life = None

def initialize_ai_life(data_dir: str = "ai_life_data") -> AILifeFoundation:
    """Initialisiert das AI Life System"""
    global ai_life
    ai_life = AILifeFoundation(data_dir)
    return ai_life

def get_ai_life() -> Optional[AILifeFoundation]:
    """Gibt aktuelle AI Life Instanz zurück"""
    return ai_life
