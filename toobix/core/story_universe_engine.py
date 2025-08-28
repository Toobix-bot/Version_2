"""
Story Universe Engine - Phase 5.3
Persistente Meta-Game Mechaniken die echte Toobix-Funktionen beeinflussen
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

@dataclass
class StoryCharacter:
    """Persistenter Story-Charakter mit Progression"""
    name: str
    level: int = 1
    experience: int = 0
    health: int = 100
    energy: int = 100
    skills: Dict[str, int] = None
    inventory: List[str] = None
    achievements: List[str] = None
    story_progress: Dict[str, Any] = None
    last_activity: str = ""
    total_playtime: int = 0  # in Minuten
    
    def __post_init__(self):
        if self.skills is None:
            self.skills = {
                "productivity": 1,
                "creativity": 1, 
                "wellness": 1,
                "technical": 1,
                "social": 1
            }
        if self.inventory is None:
            self.inventory = ["welcome_gift"]
        if self.achievements is None:
            self.achievements = []
        if self.story_progress is None:
            self.story_progress = {"current_chapter": "prologue", "completed_quests": []}

@dataclass
class StoryItem:
    """Sammelbare Items im Story Universe"""
    id: str
    name: str
    description: str
    rarity: str  # common, rare, epic, legendary
    category: str  # tool, consumable, cosmetic, unlock
    effect: Dict[str, Any] = None
    unlock_condition: str = ""
    
    def __post_init__(self):
        if self.effect is None:
            self.effect = {}

@dataclass
class StoryQuest:
    """Story-Quests die Toobix-Features integrieren"""
    id: str
    title: str
    description: str
    chapter: str
    objectives: List[str]
    rewards: Dict[str, Any]
    completion_condition: str
    real_world_integration: str  # Welche Toobix-Funktion wird aktiviert
    difficulty: str = "normal"
    estimated_time: int = 15  # Minuten
    is_completed: bool = False
    
    def __post_init__(self):
        if self.rewards is None:
            self.rewards = {"experience": 100, "items": []}

@dataclass
class StoryChapter:
    """Story-Kapitel mit progressiven Freischaltungen"""
    id: str
    title: str
    description: str
    unlock_level: int
    quests: List[str]
    unlocked_features: List[str]  # Toobix-Features die freigeschaltet werden
    background_story: str
    is_unlocked: bool = False

class StoryUniverseEngine:
    """
    Story Universe Engine - Persistente Meta-Game Mechaniken
    Verbindet interaktive Geschichten mit echten Toobix-Funktionen
    """
    
    def __init__(self):
        self.save_file = Path("toobix_story_save.json")
        self.character: Optional[StoryCharacter] = None
        self.items_database: Dict[str, StoryItem] = {}
        self.quests_database: Dict[str, StoryQuest] = {}
        self.chapters_database: Dict[str, StoryChapter] = {}
        self.active_story_mode = False
        self.current_scene = None
        self.story_callbacks: Dict[str, Callable] = {}
        
        self._initialize_story_content()
        self._load_save_data()
        logger.info("🎮 Story Universe Engine initialisiert")
    
    def _initialize_story_content(self):
        """Initialisiert alle Story-Inhalte"""
        self._create_items_database()
        self._create_quests_database()
        self._create_chapters_database()
    
    def _create_items_database(self):
        """Erstellt die Items-Datenbank"""
        items = [
            # Starter Items
            StoryItem("welcome_gift", "🎁 Willkommensgeschenk", 
                     "Ein geheimnisvolles Geschenk von Toobix", "common", "consumable",
                     {"experience": 50, "energy": 20}),
            
            # Productivity Items
            StoryItem("focus_crystal", "💎 Fokus-Kristall",
                     "Erhöht deine Konzentrationsfähigkeit", "rare", "tool",
                     {"productivity_boost": 25, "focus_duration": 30}),
            
            StoryItem("time_weaver", "⏰ Zeit-Weber",
                     "Macht dir Zeit-Management zu einer Kunst", "epic", "tool",
                     {"time_efficiency": 40, "unlocks": ["advanced_scheduler"]}),
            
            # Creativity Items  
            StoryItem("inspiration_feather", "🪶 Inspirations-Feder",
                     "Entfacht kreative Flammen in deinem Geist", "rare", "tool",
                     {"creativity_boost": 30, "idea_generation": True}),
            
            StoryItem("muse_voice", "🎵 Musen-Stimme", 
                     "Verleiht deinen Worten magische Kraft", "legendary", "tool",
                     {"writing_enhancement": 50, "unlocks": ["creative_assistant"]}),
            
            # Wellness Items
            StoryItem("zen_stone", "🪨 Zen-Stein",
                     "Bringt innere Ruhe und Balance", "common", "consumable",
                     {"stress_reduction": 20, "meditation_bonus": 15}),
            
            StoryItem("harmony_bell", "🔔 Harmonie-Glocke",
                     "Läutet eine Ära des Wohlbefindens ein", "epic", "tool",
                     {"wellness_mastery": 35, "unlocks": ["advanced_meditation"]}),
            
            # Technical Items
            StoryItem("code_scroll", "📜 Code-Rolle",
                     "Antike Weisheiten der Programmierung", "rare", "tool",
                     {"technical_skill": 25, "debugging_power": True}),
            
            StoryItem("system_crown", "👑 System-Krone",
                     "Macht dich zum Herrscher über alle Systeme", "legendary", "unlock",
                     {"admin_privileges": True, "unlocks": ["god_mode"]}),
            
            # Social Items
            StoryItem("empathy_gem", "💙 Empathie-Juwel",
                     "Verstärkt deine zwischenmenschlichen Fähigkeiten", "rare", "tool",
                     {"social_boost": 30, "communication_enhancement": True}),
            
            # Cosmetic Items
            StoryItem("star_badge", "⭐ Stern-Abzeichen",
                     "Symbol für außergewöhnliche Leistungen", "rare", "cosmetic",
                     {"prestige": 10, "visual_effect": "sparkling"}),
            
            StoryItem("rainbow_aura", "🌈 Regenbogen-Aura",
                     "Umhüllt dich mit farbenfroher Energie", "epic", "cosmetic",
                     {"mood_boost": 25, "visual_effect": "rainbow_glow"})
        ]
        
        for item in items:
            self.items_database[item.id] = item
    
    def _create_quests_database(self):
        """Erstellt die Quests-Datenbank"""
        quests = [
            # Prologue Quests
            StoryQuest("first_words", "🗣️ Erste Worte",
                      "Sprich zum ersten Mal mit Toobix und entdecke die Macht der Stimme",
                      "prologue", 
                      ["Aktiviere Spracheingabe", "Sage 'Hallo Toobix'", "Erhalte eine Antwort"],
                      {"experience": 100, "items": ["focus_crystal"], "unlocks": ["voice_commands"]},
                      "voice_interaction_completed", "speech_engine"),
            
            StoryQuest("digital_awakening", "💻 Digitales Erwachen", 
                      "Erforsche die grundlegenden Toobix-Fähigkeiten",
                      "prologue",
                      ["Öffne System-Überwachung", "Prüfe Systemstatus", "Führe erste Analyse durch"],
                      {"experience": 150, "items": ["zen_stone"], "unlocks": ["system_monitoring"]},
                      "system_analysis_completed", "system_monitor"),
            
            StoryQuest("knowledge_seeker", "📚 Wissenssucher",
                      "Entdecke die Geheimnisse der Toobix-Wissensbasis",
                      "prologue",
                      ["Öffne Knowledge Discovery Center", "Browse 3 verschiedene Kategorien", "Probiere ein Feature aus"],
                      {"experience": 200, "items": ["code_scroll"], "unlocks": ["knowledge_center"]},
                      "knowledge_exploration_completed", "knowledge_discovery"),
            
            # Chapter 1 Quests
            StoryQuest("productivity_master", "⚡ Produktivitäts-Meister",
                      "Meistere die Kunst der effizienten Arbeitsorganisation",
                      "chapter_1",
                      ["Aktiviere Smart Suggestions", "Nutze 5 verschiedene Suggestions", "Organisiere deine Dateien"],
                      {"experience": 300, "items": ["time_weaver"], "unlocks": ["advanced_automation"]},
                      "productivity_mastery_achieved", "productivity_tools"),
            
            StoryQuest("wellness_guardian", "🧘 Wellness-Wächter",
                      "Werde zum Hüter deines digitalen Wohlbefindens", 
                      "chapter_1",
                      ["Starte eine Meditation", "Führe Atemübungen durch", "Nutze Soundscapes"],
                      {"experience": 250, "items": ["harmony_bell"], "unlocks": ["advanced_wellness"]},
                      "wellness_mastery_achieved", "wellness_engine"),
            
            StoryQuest("creative_spark", "🎨 Kreativer Funke",
                      "Entfache die kreativen Flammen in deinem digitalen Raum",
                      "chapter_1", 
                      ["Nutze KI für kreative Aufgaben", "Erstelle ein Projekt", "Teile deine Kreation"],
                      {"experience": 350, "items": ["inspiration_feather", "muse_voice"], "unlocks": ["creative_suite"]},
                      "creativity_unleashed", "creative_tools"),
            
            # Chapter 2 Quests
            StoryQuest("system_sage", "🔮 System-Weiser",
                      "Erlange tiefe Einsichten in die Geheimnisse digitaler Systeme",
                      "chapter_2",
                      ["Führe Deep Analytics durch", "Verstehe Systemkorrelationen", "Optimiere Performance"],
                      {"experience": 500, "items": ["system_crown"], "unlocks": ["god_mode"]},
                      "system_mastery_achieved", "deep_analytics"),
            
            StoryQuest("social_architect", "🤝 Sozialer Architekt",
                      "Baue Brücken zwischen digitaler und menschlicher Welt",
                      "chapter_2",
                      ["Nutze Kollaborations-Features", "Teile Wissen", "Hilf anderen Nutzern"],
                      {"experience": 400, "items": ["empathy_gem", "rainbow_aura"], "unlocks": ["social_features"]},
                      "social_mastery_achieved", "collaboration_tools")
        ]
        
        for quest in quests:
            self.quests_database[quest.id] = quest
    
    def _create_chapters_database(self):
        """Erstellt die Kapitel-Datenbank"""
        chapters = [
            StoryChapter("prologue", "🌅 Prolog: Das Erwachen",
                        "Deine Reise in das Toobix-Universum beginnt...",
                        1, ["first_words", "digital_awakening", "knowledge_seeker"],
                        ["basic_features", "voice_control", "knowledge_access"],
                        """Du erwachst in einer digitalen Welt voller Möglichkeiten. 
                        Toobix, ein mysteriöser KI-Begleiter, lädt dich ein, die Geheimnisse 
                        produktiver und kreativer digitaler Existenz zu entdecken."""),
            
            StoryChapter("chapter_1", "⚡ Kapitel 1: Die Meisterschaft",
                        "Entwickle deine grundlegenden Fähigkeiten zur Perfektion",
                        3, ["productivity_master", "wellness_guardian", "creative_spark"],
                        ["advanced_automation", "wellness_mastery", "creative_suite"],
                        """Mit grundlegenden Kenntnissen ausgerüstet, tauchst du tiefer ein. 
                        Drei Pfade öffnen sich vor dir: Der Weg der Produktivität, 
                        der Pfad des Wohlbefindens und die Straße der Kreativität."""),
            
            StoryChapter("chapter_2", "🔮 Kapitel 2: Die Transzendenz", 
                        "Überschreite die Grenzen zwischen digital und real",
                        7, ["system_sage", "social_architect"],
                        ["god_mode", "reality_integration", "social_mastery"],
                        """Du näherst dich der ultimativen Harmonie zwischen Mensch und System. 
                        Hier lernst du, nicht nur Toobix zu nutzen, sondern eins mit ihm zu werden."""),
            
            StoryChapter("chapter_3", "🌟 Kapitel 3: Die Unendlichkeit",
                        "Werde zum Schöpfer deiner digitalen Realität", 
                        12, [],
                        ["universe_creation", "reality_shaping", "infinite_potential"],
                        """Die finale Transformation. Du wirst vom Nutzer zum Schöpfer, 
                        vom Lernenden zum Meister, vom Menschen zum digitalen Gott.""")
        ]
        
        for chapter in chapters:
            self.chapters_database[chapter.id] = chapter
    
    def _load_save_data(self):
        """Lädt gespeicherte Story-Daten"""
        try:
            if self.save_file.exists():
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Character laden
                if 'character' in data:
                    char_data = data['character']
                    self.character = StoryCharacter(**char_data)
                else:
                    self._create_new_character()
                
                # Quest-Fortschritte aktualisieren
                if 'quest_progress' in data:
                    for quest_id, progress in data['quest_progress'].items():
                        if quest_id in self.quests_database:
                            self.quests_database[quest_id].is_completed = progress.get('completed', False)
                
                # Kapitel-Freischaltungen
                if 'chapter_progress' in data:
                    for chapter_id, unlocked in data['chapter_progress'].items():
                        if chapter_id in self.chapters_database:
                            self.chapters_database[chapter_id].is_unlocked = unlocked
                
                logger.info(f"Story-Daten geladen: Level {self.character.level}, {len(self.character.achievements)} Achievements")
            else:
                self._create_new_character()
                
        except Exception as e:
            logger.error(f"Fehler beim Laden der Story-Daten: {e}")
            self._create_new_character()
    
    def _create_new_character(self):
        """Erstellt einen neuen Character"""
        self.character = StoryCharacter("Abenteurer")
        self.chapters_database["prologue"].is_unlocked = True
        self._save_data()
        logger.info("Neuer Story-Character erstellt")
    
    def _save_data(self):
        """Speichert Story-Daten"""
        try:
            data = {
                'character': asdict(self.character),
                'quest_progress': {
                    quest_id: {'completed': quest.is_completed}
                    for quest_id, quest in self.quests_database.items()
                },
                'chapter_progress': {
                    chapter_id: chapter.is_unlocked
                    for chapter_id, chapter in self.chapters_database.items()
                },
                'last_save': datetime.now().isoformat()
            }
            
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Story-Daten: {e}")
    
    def register_story_callback(self, action: str, callback: Callable):
        """Registriert Callbacks für Story-Aktionen"""
        self.story_callbacks[action] = callback
    
    def trigger_story_event(self, event_type: str, details: Dict[str, Any] = None):
        """Triggert Story-Events basierend auf Toobix-Nutzung"""
        if not self.character:
            return
        
        # Erfahrung für jede Aktion
        self._add_experience(10)
        
        # Spezifische Event-Behandlung
        if event_type == "voice_interaction":
            self._check_quest_completion("first_words")
        elif event_type == "system_analysis":
            self._check_quest_completion("digital_awakening")
        elif event_type == "knowledge_browsing":
            self._check_quest_completion("knowledge_seeker")
        elif event_type == "smart_suggestion_used":
            self._progress_quest("productivity_master")
        elif event_type == "meditation_started":
            self._check_quest_completion("wellness_guardian")
        elif event_type == "creative_task":
            self._check_quest_completion("creative_spark")
        elif event_type == "deep_analytics":
            self._check_quest_completion("system_sage")
        elif event_type == "social_interaction":
            self._check_quest_completion("social_architect")
        
        # Item-Nutzung verarbeiten
        if details and "item_used" in details:
            self._use_item(details["item_used"])
        
        self._save_data()
    
    def _add_experience(self, amount: int):
        """Fügt Erfahrung hinzu und prüft Level-Ups"""
        if not self.character:
            return
        
        old_level = self.character.level
        self.character.experience += amount
        
        # Level-Up Berechnung (exponentiell)
        new_level = int((self.character.experience / 100) ** 0.7) + 1
        
        if new_level > old_level:
            self.character.level = new_level
            self._handle_level_up(old_level, new_level)
    
    def _handle_level_up(self, old_level: int, new_level: int):
        """Behandelt Level-Ups"""
        logger.info(f"LEVEL UP! {old_level} → {new_level}")
        
        # Skill-Punkte verteilen
        skill_points = new_level - old_level
        skills = list(self.character.skills.keys())
        for _ in range(skill_points):
            random_skill = random.choice(skills)
            self.character.skills[random_skill] += 1
        
        # Neue Kapitel freischalten
        for chapter in self.chapters_database.values():
            if not chapter.is_unlocked and new_level >= chapter.unlock_level:
                chapter.is_unlocked = True
                self._unlock_chapter(chapter)
        
        # Callback für GUI
        if "level_up" in self.story_callbacks:
            self.story_callbacks["level_up"](old_level, new_level)
    
    def _unlock_chapter(self, chapter: StoryChapter):
        """Schaltet ein neues Kapitel frei"""
        logger.info(f"Neues Kapitel freigeschaltet: {chapter.title}")
        
        # Toobix-Features freischalten
        for feature in chapter.unlocked_features:
            if "unlock_feature" in self.story_callbacks:
                self.story_callbacks["unlock_feature"](feature)
        
        # GUI-Benachrichtigung
        if "chapter_unlocked" in self.story_callbacks:
            self.story_callbacks["chapter_unlocked"](chapter)
    
    def _check_quest_completion(self, quest_id: str):
        """Prüft und markiert Quest-Abschluss"""
        if quest_id not in self.quests_database:
            return
        
        quest = self.quests_database[quest_id]
        if quest.is_completed:
            return
        
        quest.is_completed = True
        self._complete_quest(quest)
    
    def _progress_quest(self, quest_id: str):
        """Macht Fortschritt bei einer Quest"""
        # Hier könnte komplexere Quest-Logik implementiert werden
        pass
    
    def _complete_quest(self, quest: StoryQuest):
        """Behandelt Quest-Abschluss"""
        logger.info(f"Quest abgeschlossen: {quest.title}")
        
        # Rewards vergeben
        if "experience" in quest.rewards:
            self._add_experience(quest.rewards["experience"])
        
        if "items" in quest.rewards:
            for item_id in quest.rewards["items"]:
                self._add_item_to_inventory(item_id)
        
        if "unlocks" in quest.rewards:
            for unlock in quest.rewards["unlocks"]:
                if "unlock_feature" in self.story_callbacks:
                    self.story_callbacks["unlock_feature"](unlock)
        
        # Achievement hinzufügen
        achievement = f"quest_completed_{quest.id}"
        if achievement not in self.character.achievements:
            self.character.achievements.append(achievement)
        
        # GUI-Benachrichtigung
        if "quest_completed" in self.story_callbacks:
            self.story_callbacks["quest_completed"](quest)
    
    def _add_item_to_inventory(self, item_id: str):
        """Fügt Item zum Inventar hinzu"""
        if item_id in self.items_database and item_id not in self.character.inventory:
            self.character.inventory.append(item_id)
            logger.info(f"Neues Item erhalten: {self.items_database[item_id].name}")
            
            if "item_received" in self.story_callbacks:
                self.story_callbacks["item_received"](self.items_database[item_id])
    
    def _use_item(self, item_id: str):
        """Nutzt ein Item aus dem Inventar"""
        if item_id not in self.character.inventory or item_id not in self.items_database:
            return
        
        item = self.items_database[item_id]
        
        # Item-Effekte anwenden
        if "experience" in item.effect:
            self._add_experience(item.effect["experience"])
        
        if "energy" in item.effect:
            self.character.energy = min(100, self.character.energy + item.effect["energy"])
        
        if "unlocks" in item.effect:
            for unlock in item.effect["unlocks"]:
                if "unlock_feature" in self.story_callbacks:
                    self.story_callbacks["unlock_feature"](unlock)
        
        # Consumable Items entfernen
        if item.category == "consumable":
            self.character.inventory.remove(item_id)
        
        logger.info(f"Item genutzt: {item.name}")
        
        if "item_used" in self.story_callbacks:
            self.story_callbacks["item_used"](item)
    
    def get_character_status(self) -> Dict[str, Any]:
        """Gibt aktuellen Character-Status zurück"""
        if not self.character:
            return {}
        
        return {
            "name": self.character.name,
            "level": self.character.level,
            "experience": self.character.experience,
            "next_level_exp": ((self.character.level ** (1/0.7)) * 100),
            "health": self.character.health,
            "energy": self.character.energy,
            "skills": self.character.skills,
            "inventory_count": len(self.character.inventory),
            "achievements_count": len(self.character.achievements),
            "current_chapter": self.character.story_progress.get("current_chapter", "prologue")
        }
    
    def get_available_quests(self) -> List[StoryQuest]:
        """Gibt verfügbare Quests zurück"""
        available = []
        for quest in self.quests_database.values():
            # Prüfe ob Chapter freigeschaltet ist
            chapter = self.chapters_database.get(quest.chapter)
            if chapter and chapter.is_unlocked and not quest.is_completed:
                available.append(quest)
        return available
    
    def get_inventory_items(self) -> List[StoryItem]:
        """Gibt Inventar-Items zurück"""
        if not self.character:
            return []
        
        return [self.items_database[item_id] for item_id in self.character.inventory 
                if item_id in self.items_database]
    
    def get_unlocked_chapters(self) -> List[StoryChapter]:
        """Gibt freigeschaltete Kapitel zurück"""
        return [chapter for chapter in self.chapters_database.values() if chapter.is_unlocked]
    
    def start_story_mode(self):
        """Startet den interaktiven Story-Modus"""
        self.active_story_mode = True
        current_chapter = self.character.story_progress.get("current_chapter", "prologue")
        
        if "story_mode_started" in self.story_callbacks:
            self.story_callbacks["story_mode_started"](current_chapter)
    
    def stop_story_mode(self):
        """Beendet den Story-Modus"""
        self.active_story_mode = False
        
        if "story_mode_stopped" in self.story_callbacks:
            self.story_callbacks["story_mode_stopped"]()
    
    def get_story_summary(self) -> Dict[str, Any]:
        """Gibt Story-Zusammenfassung zurück"""
        if not self.character:
            return {}
        
        completed_quests = [q for q in self.quests_database.values() if q.is_completed]
        available_quests = self.get_available_quests()
        unlocked_chapters = self.get_unlocked_chapters()
        
        return {
            "character": self.get_character_status(),
            "completed_quests": len(completed_quests),
            "available_quests": len(available_quests),
            "unlocked_chapters": len(unlocked_chapters),
            "total_chapters": len(self.chapters_database),
            "inventory_items": len(self.character.inventory),
            "achievements": len(self.character.achievements),
            "story_mode_active": self.active_story_mode
        }
    
    def trigger_event(self, event_type: str) -> bool:
        """Triggert ein Story Event basierend auf realer Toobix-Aktivität"""
        try:
            if not self.character:
                return False
                
            # Event-basierte Erfahrungspunkte
            xp_rewards = {
                'task_completed': 50,
                'code_written': 30,
                'ai_query': 20,
                'system_monitored': 25,
                'git_action': 40,
                'wellness_activity': 35,
                'meditation_completed': 60,
                'breathing_exercise': 45,
                'focus_session': 55,
                'learning_activity': 70
            }
            
            if event_type in xp_rewards:
                xp_gained = xp_rewards[event_type]
                old_level = self.character.level
                
                # Erfahrung hinzufügen
                self.character.experience += xp_gained
                
                # Level-up prüfen
                while self.character.experience >= self._calculate_required_xp(self.character.level):
                    self.character.experience -= self._calculate_required_xp(self.character.level)
                    self.character.level += 1
                    
                    # Level-up Belohnungen
                    self.character.health = min(100, self.character.health + 10)
                    self.character.energy = min(100, self.character.energy + 15)
                
                # Spezielle Event-Effekte
                self._apply_event_effects(event_type)
                
                # Auto-save
                try:
                    self._save_to_file()
                except:
                    pass
                
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Fehler beim Event-Trigger: {e}")
            return False
    
    def _apply_event_effects(self, event_type: str):
        """Wendet spezielle Effekte für bestimmte Events an"""
        try:
            # Wellness-Events regenerieren
            if event_type in ['wellness_activity', 'meditation_completed', 'breathing_exercise']:
                self.character.energy = min(100, self.character.energy + 20)
                if 'wellness' in self.character.skills:
                    self.character.skills['wellness'] = min(100, self.character.skills['wellness'] + 2)
            
            # Produktivitäts-Events verbrauchen Energie aber geben Focus
            elif event_type in ['task_completed', 'code_written', 'git_action']:
                self.character.energy = max(0, self.character.energy - 5)
                if 'productivity' in self.character.skills:
                    self.character.skills['productivity'] = min(100, self.character.skills['productivity'] + 2)
            
            # AI-Queries erhöhen Creativity
            elif event_type == 'ai_query':
                if 'creativity' in self.character.skills:
                    self.character.skills['creativity'] = min(100, self.character.skills['creativity'] + 1)
            
            # System-Monitoring erhöht Technical Skills
            elif event_type == 'system_monitored':
                if 'technical' in self.character.skills:
                    self.character.skills['technical'] = min(100, self.character.skills['technical'] + 1)
            
        except Exception as e:
            logger.error(f"Fehler bei Event-Effekten: {e}")
    
    def _calculate_required_xp(self, level: int) -> int:
        """Berechnet benötigte XP für nächstes Level"""
        return int(100 * (1.5 ** (level - 1)))
    
    def _save_to_file(self):
        """Speichert Charakter-Daten"""
        try:
            if self.character:
                # Verwende das bestehende save_file
                with open(self.save_file, 'w', encoding='utf-8') as f:
                    json.dump(asdict(self.character), f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Save error: {e}")
