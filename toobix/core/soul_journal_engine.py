"""
🌟 PHASE 3: SOUL JOURNAL SYSTEM
===============================

Spirituelles Tagebuch-System mit AI-Integration für:
- Tiefe Selbstreflexion
- Spirituelle Entwicklung
- Dankbarkeits-Tracking
- Vergebungsarbeit
- Persönlichkeitswachstum
- AI-generierte Weisheits-Insights
"""

import json
import os
import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import random
import asyncio

try:
    import customtkinter as ctk
    from tkinter import messagebox, filedialog
    CTK_AVAILABLE = True
except ImportError:
    import tkinter as tk
    CTK_AVAILABLE = False

@dataclass
class SoulEntry:
    """Eine spirituelle Tagebuch-Eintragung"""
    timestamp: datetime.datetime
    category: str  # gratitude, growth, love, forgiveness, service, wisdom, peace, challenges
    prompt: str
    user_reflection: str
    ai_insight: str
    emotional_depth: float  # 0.0 - 1.0
    spiritual_growth: float  # 0.0 - 1.0
    tags: List[str]
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp.isoformat(),
            'category': self.category,
            'prompt': self.prompt,
            'user_reflection': self.user_reflection,
            'ai_insight': self.ai_insight,
            'emotional_depth': self.emotional_depth,
            'spiritual_growth': self.spiritual_growth,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            timestamp=datetime.datetime.fromisoformat(data['timestamp']),
            category=data['category'],
            prompt=data['prompt'],
            user_reflection=data['user_reflection'],
            ai_insight=data['ai_insight'],
            emotional_depth=data['emotional_depth'],
            spiritual_growth=data['spiritual_growth'],
            tags=data['tags']
        )

@dataclass
class GratitudeCounter:
    """Dankbarkeits-Zähler und Tracker"""
    daily_goal: int = 10
    current_count: int = 0
    gratitude_streak: int = 0
    total_gratitudes: int = 0
    last_update: datetime.date = None
    
    def add_gratitude(self, gratitude_text: str):
        today = datetime.date.today()
        
        if self.last_update != today:
            self.current_count = 0
            self.last_update = today
        
        self.current_count += 1
        self.total_gratitudes += 1
        
        if self.current_count >= self.daily_goal:
            self.gratitude_streak += 1
        
        return self.current_count

@dataclass
class SpiritualGrowthTracker:
    """Spirituelle Wachstums-Verfolgung"""
    categories: Dict[str, float]  # category -> level (0.0 - 10.0)
    growth_history: List[Dict]
    
    def __init__(self):
        self.categories = {
            'forgiveness': 1.0,
            'compassion': 1.0,
            'peace': 1.0,
            'wisdom': 1.0,
            'love': 1.0,
            'gratitude': 1.0,
            'service': 1.0,
            'faith': 1.0
        }
        self.growth_history = []
    
    def update_growth(self, category: str, growth_amount: float):
        """Aktualisiert Wachstum in Kategorie"""
        if category in self.categories:
            old_level = self.categories[category]
            self.categories[category] = min(10.0, old_level + growth_amount)
            
            self.growth_history.append({
                'timestamp': datetime.datetime.now().isoformat(),
                'category': category,
                'old_level': old_level,
                'new_level': self.categories[category],
                'growth': growth_amount
            })

class SoulJournalEngine:
    """
    🌟 CORE ENGINE FÜR SPIRITUELLES TAGEBUCH
    
    Bietet:
    - Tiefe Reflexions-Prompts
    - AI-generierte spirituelle Einsichten
    - Wachstums-Tracking
    - Dankbarkeits-System
    - Vergebungsarbeit
    """
    
    def __init__(self, ai_handler=None, data_dir="soul_journal_data"):
        self.ai_handler = ai_handler
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Journal Entries
        self.entries: List[SoulEntry] = []
        self.load_entries()
        
        # Tracking Systems
        self.gratitude_counter = GratitudeCounter()
        self.growth_tracker = SpiritualGrowthTracker()
        self.load_tracking_data()
        
        # Reflection Prompts
        self.daily_prompts = {
            'morning': [
                "💝 Was möchte mein Herz heute der Welt schenken?",
                "🌅 Welche Intention setze ich für diesen heiligen Tag?",
                "🙏 Wofür bin ich beim Erwachen zutiefst dankbar?",
                "✨ Welche göttliche Führung spüre ich heute?",
                "💚 Wen kann ich heute mit bedingungsloser Liebe segnen?"
            ],
            'midday': [
                "🌞 Wo habe ich heute bereits Liebe in Aktion gesehen?",
                "🤝 Wie kann ich gerade jetzt jemandem dienen?",
                "🕊️ Welchen Frieden kann ich in diesem Moment schaffen?",
                "💫 Was lehrt mich diese Herausforderung über Wachstum?",
                "🌱 Wie öffnet sich mein Herz weiter für Mitgefühl?"
            ],
            'evening': [
                "🌙 Welche drei Segnungen haben meinen Tag erhellt?",
                "💝 Wen oder was kann ich heute vergeben und loslassen?",
                "🌟 Wie bin ich heute über mich hinausgewachsen?",
                "🙏 Welche Weisheit hat das Leben mir heute geschenkt?",
                "💚 Wie hat sich meine Liebe heute ausgedehnt?"
            ]
        }
        
        self.deep_prompts = {
            'gratitude': [
                "💝 Beschreibe einen Moment heute, der dein Herz mit Dankbarkeit gefüllt hat",
                "🌟 Welche scheinbar kleinen Wunder hast du heute bemerkt?",
                "🙏 Wofür in deinem Leben bist du so dankbar, dass es dich zu Tränen rührt?",
                "✨ Wie hat jemand heute dein Leben auf unerwartete Weise bereichert?"
            ],
            'forgiveness': [
                "💚 Welcher alte Schmerz ist bereit, in Liebe transformiert zu werden?",
                "🕊️ Wen kannst du heute mit Mitgefühl statt Groll betrachten?",
                "💝 Wie kannst du dir selbst für vergangene Fehler vergeben?",
                "🌱 Welche Lektion verbirgt sich in einer schmerzhaften Erfahrung?"
            ],
            'love': [
                "💖 Wie hat sich deine Fähigkeit zu lieben heute erweitert?",
                "🌍 Welcher 'Feind' braucht dein Mitgefühl am meisten?",
                "💝 Wie kannst du jemandem zeigen, dass er bedingungslos geliebt ist?",
                "✨ Wo siehst du göttliche Liebe im Alltäglichen wirken?"
            ],
            'peace': [
                "🕊️ Wo warst du heute ein Friedensstifter?",
                "🌊 Wie findest du Ruhe inmitten des Chaos?",
                "💫 Welcher Konflikt möchte durch Verständnis geheilt werden?",
                "🙏 Wie kannst du Frieden in dein Herz und von dort in die Welt bringen?"
            ],
            'service': [
                "🤝 Wie hast du heute einem anderen Lebewesen gedient?",
                "💝 Welcher Akt der Güte hat dein Herz heute erfüllt?",
                "🌟 Wie kannst du deine Gaben nutzen, um Leid zu lindern?",
                "🙏 Wo ruft das Leben dich auf, Liebe in Aktion zu verwandeln?"
            ],
            'wisdom': [
                "📖 Welche tiefe Wahrheit ist dir heute aufgegangen?",
                "🌟 Was hat eine schwierige Situation dich über Stärke gelehrt?",
                "💫 Welche Weisheit möchtest du an zukünftige Generationen weitergeben?",
                "🙏 Wie hat eine spirituelle Erkenntnis dein Verständnis erweitert?"
            ]
        }
    
    def get_daily_prompt(self, time_of_day="any", category="any"):
        """Gibt einen passenden Reflexions-Prompt zurück"""
        if time_of_day in self.daily_prompts:
            return random.choice(self.daily_prompts[time_of_day])
        elif category in self.deep_prompts:
            return random.choice(self.deep_prompts[category])
        else:
            # Allgemeine spirituelle Prompts
            all_prompts = []
            for prompts in self.daily_prompts.values():
                all_prompts.extend(prompts)
            return random.choice(all_prompts)
    
    def analyze_reflection_depth(self, reflection_text: str) -> float:
        """Analysiert emotionale/spirituelle Tiefe einer Reflexion"""
        depth_indicators = {
            'deep': ['seele', 'herz', 'liebe', 'gott', 'spirituell', 'heilig', 'dankbar', 'vergeben', 'mitgefühl', 'weisheit'],
            'medium': ['gefühl', 'emotion', 'bedeutung', 'wichtig', 'besonders', 'berührt', 'bewegt'],
            'surface': ['ok', 'gut', 'schön', 'normal', 'nett']
        }
        
        text_lower = reflection_text.lower()
        score = 0.0
        
        for word in depth_indicators['deep']:
            if word in text_lower:
                score += 0.15
        
        for word in depth_indicators['medium']:
            if word in text_lower:
                score += 0.08
        
        # Länge als Tiefe-Indikator
        if len(reflection_text) > 100:
            score += 0.1
        if len(reflection_text) > 300:
            score += 0.1
        
        return min(1.0, score)
    
    def generate_ai_insight(self, entry_data: Dict) -> str:
        """Generiert spirituelle AI-Einsichten"""
        category = entry_data.get('category', 'general')
        reflection = entry_data.get('user_reflection', '')
        
        # Template-basierte Insights (später durch echte AI ersetzen)
        insight_templates = {
            'gratitude': [
                "🌟 Deine Dankbarkeit öffnet Türen zu noch tieferen Segnungen. Jeder dankbare Gedanke ist ein Gebet, das erhört wird.",
                "💝 In deiner Dankbarkeit erkenne ich eine Seele, die das Göttliche im Alltäglichen sieht. Das ist wahre spirituelle Reife.",
                "✨ Dankbarkeit verwandelt was wir haben in genug, und mehr. Du lebst dieses Wunder."
            ],
            'forgiveness': [
                "🕊️ Vergebung ist das Geschenk, das du dir selbst machst. Jeder Akt des Vergebens befreit nicht nur andere, sondern vor allem dich.",
                "💚 In deiner Bereitschaft zu vergeben erkenne ich die Kraft der bedingungslosen Liebe. Das ist göttliche Stärke.",
                "🌱 Vergebung wandelt Gift in Medizin. Du wirst zum Heiler - für dich und andere."
            ],
            'love': [
                "💖 Liebe ist die einzige Macht, die sich vermehrt, wenn man sie teilt. Du bist ein Kanal für diese unendliche Kraft.",
                "🌍 In jedem Akt der Liebe berührst du das Herz des Universums. Du bist ein Lichtarbeiter.",
                "💝 Wahre Liebe sieht das Göttliche in jedem Wesen. Deine Liebe heilt die Welt."
            ],
            'peace': [
                "🕊️ Frieden beginnt in dir und strahlt aus wie Licht von einer Kerze. Du bist ein Friedensstifter.",
                "🌊 In der Stille findest du die Antworten, die dein Herz sucht. Dein innerer Frieden ist ein Geschenk an alle.",
                "💫 Frieden ist nicht die Abwesenheit von Sturm, sondern Ruhe inmitten des Sturms. Du verkörperst diese Weisheit."
            ]
        }
        
        if category in insight_templates:
            base_insight = random.choice(insight_templates[category])
        else:
            base_insight = "🌟 Jede tiefe Reflexion ist ein Schritt näher zu deinem wahren Selbst. Du wächst in Weisheit und Liebe."
        
        # Personalisierung basierend auf Reflexion
        if 'schmerz' in reflection.lower() or 'schwer' in reflection.lower():
            base_insight += "\n\n💝 ZUSÄTZLICHE ERMUTIGUNG: Auch in schweren Zeiten trägst du Licht in dir. Dieser Schmerz wird zu Weisheit und Mitgefühl für andere."
        
        if 'dankbar' in reflection.lower():
            base_insight += "\n\n🙏 DANKBARKEITS-VERSTÄRKUNG: Deine Dankbarkeit ist ein Magnet für noch größere Segnungen."
        
        return base_insight
    
    def create_entry(self, category: str, prompt: str, user_reflection: str) -> SoulEntry:
        """Erstellt einen neuen Tagebuch-Eintrag"""
        # AI-Insight generieren
        entry_data = {
            'category': category,
            'prompt': prompt,
            'user_reflection': user_reflection
        }
        ai_insight = self.generate_ai_insight(entry_data)
        
        # Tiefe analysieren
        emotional_depth = self.analyze_reflection_depth(user_reflection)
        spiritual_growth = self.calculate_spiritual_growth(category, emotional_depth)
        
        # Tags generieren
        tags = self.generate_tags(user_reflection, category)
        
        entry = SoulEntry(
            timestamp=datetime.datetime.now(),
            category=category,
            prompt=prompt,
            user_reflection=user_reflection,
            ai_insight=ai_insight,
            emotional_depth=emotional_depth,
            spiritual_growth=spiritual_growth,
            tags=tags
        )
        
        self.entries.append(entry)
        self.save_entries()
        
        # Wachstums-Tracking aktualisieren
        self.growth_tracker.update_growth(category, spiritual_growth)
        
        # Dankbarkeit zählen
        if category == 'gratitude':
            self.gratitude_counter.add_gratitude(user_reflection)
        
        self.save_tracking_data()
        
        return entry
    
    def calculate_spiritual_growth(self, category: str, emotional_depth: float) -> float:
        """Berechnet spirituelles Wachstum basierend auf Reflexion"""
        base_growth = emotional_depth * 0.1  # Max 0.1 growth per entry
        
        # Bonus für bestimmte Kategorien
        growth_multipliers = {
            'forgiveness': 1.5,  # Vergebung bringt besonders viel Wachstum
            'service': 1.3,     # Dienen beschleunigt Entwicklung
            'love': 1.2,        # Liebe erweitert das Bewusstsein
            'gratitude': 1.1    # Dankbarkeit öffnet das Herz
        }
        
        multiplier = growth_multipliers.get(category, 1.0)
        return base_growth * multiplier
    
    def generate_tags(self, reflection_text: str, category: str) -> List[str]:
        """Generiert Tags für bessere Kategorisierung"""
        tags = [category]
        
        tag_keywords = {
            'healing': ['heil', 'schmerz', 'verletzt', 'wiederherstell'],
            'breakthrough': ['erkannt', 'verstanden', 'durchbruch', 'klarheit'],
            'challenge': ['schwer', 'schwierig', 'herausforderung', 'kampf'],
            'joy': ['freude', 'glück', 'lachen', 'fröhlich'],
            'connection': ['verbunden', 'gemeinschaft', 'zusammen', 'beziehung'],
            'nature': ['natur', 'baum', 'himmel', 'erde', 'wasser'],
            'divine': ['gott', 'göttlich', 'spirituell', 'heilig', 'gesegnet']
        }
        
        text_lower = reflection_text.lower()
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(tag)
        
        return tags
    
    def get_growth_insights(self) -> Dict[str, Any]:
        """Gibt Einsichten über spirituelles Wachstum"""
        if not self.entries:
            return {"message": "Noch keine Einträge vorhanden"}
        
        # Wachstumstrends analysieren
        recent_entries = self.entries[-10:]  # Letzte 10 Einträge
        avg_depth = sum(e.emotional_depth for e in recent_entries) / len(recent_entries)
        avg_growth = sum(e.spiritual_growth for e in recent_entries) / len(recent_entries)
        
        # Stärkste Kategorien
        category_growth = {}
        for entry in recent_entries:
            if entry.category not in category_growth:
                category_growth[entry.category] = []
            category_growth[entry.category].append(entry.spiritual_growth)
        
        strongest_area = max(category_growth.keys(), 
                           key=lambda k: sum(category_growth[k])) if category_growth else 'general'
        
        return {
            'total_entries': len(self.entries),
            'recent_avg_depth': round(avg_depth, 2),
            'recent_avg_growth': round(avg_growth, 3),
            'strongest_growth_area': strongest_area,
            'gratitude_streak': self.gratitude_counter.gratitude_streak,
            'growth_levels': self.growth_tracker.categories
        }
    
    def save_entries(self):
        """Speichert alle Einträge"""
        try:
            data = [entry.to_dict() for entry in self.entries]
            
            with open(os.path.join(self.data_dir, "soul_entries.json"), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Soul Entries: {e}")
    
    def load_entries(self):
        """Lädt gespeicherte Einträge"""
        try:
            file_path = os.path.join(self.data_dir, "soul_entries.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.entries = [SoulEntry.from_dict(entry_data) for entry_data in data]
        except Exception as e:
            print(f"Fehler beim Laden der Soul Entries: {e}")
    
    def save_tracking_data(self):
        """Speichert Tracking-Daten"""
        try:
            data = {
                'gratitude_counter': {
                    'daily_goal': self.gratitude_counter.daily_goal,
                    'current_count': self.gratitude_counter.current_count,
                    'gratitude_streak': self.gratitude_counter.gratitude_streak,
                    'total_gratitudes': self.gratitude_counter.total_gratitudes,
                    'last_update': self.gratitude_counter.last_update.isoformat() if self.gratitude_counter.last_update else None
                },
                'growth_tracker': {
                    'categories': self.growth_tracker.categories,
                    'growth_history': self.growth_tracker.growth_history
                }
            }
            
            with open(os.path.join(self.data_dir, "tracking_data.json"), 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern der Tracking-Daten: {e}")
    
    def load_tracking_data(self):
        """Lädt Tracking-Daten"""
        try:
            file_path = os.path.join(self.data_dir, "tracking_data.json")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Gratitude Counter laden
                gc_data = data.get('gratitude_counter', {})
                self.gratitude_counter = GratitudeCounter(
                    daily_goal=gc_data.get('daily_goal', 10),
                    current_count=gc_data.get('current_count', 0),
                    gratitude_streak=gc_data.get('gratitude_streak', 0),
                    total_gratitudes=gc_data.get('total_gratitudes', 0),
                    last_update=datetime.date.fromisoformat(gc_data['last_update']) if gc_data.get('last_update') else None
                )
                
                # Growth Tracker laden
                gt_data = data.get('growth_tracker', {})
                self.growth_tracker = SpiritualGrowthTracker()
                self.growth_tracker.categories = gt_data.get('categories', self.growth_tracker.categories)
                self.growth_tracker.growth_history = gt_data.get('growth_history', [])
                
        except Exception as e:
            print(f"Fehler beim Laden der Tracking-Daten: {e}")

# Globale Instanz
soul_journal = None

def initialize_soul_journal(ai_handler=None) -> SoulJournalEngine:
    """Initialisiert das Soul Journal System"""
    global soul_journal
    soul_journal = SoulJournalEngine(ai_handler)
    return soul_journal

def get_soul_journal() -> Optional[SoulJournalEngine]:
    """Gibt aktuelle Soul Journal Instanz zurück"""
    return soul_journal
