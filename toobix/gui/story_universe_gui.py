"""
Story Universe GUI - Phase 5.3
Interaktive Story-Oberfläche mit Character-Progression
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Any, Callable, Optional
import logging

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

from toobix.core.story_universe_engine import (
    StoryUniverseEngine, 
    StoryCharacter, 
    StoryItem, 
    StoryQuest,
    StoryChapter
)

logger = logging.getLogger(__name__)

class StoryUniverseGUI:
    """
    GUI für das Story Universe System
    Bildschirm-basierte Story-Modi mit persistenter Progression
    """
    
    def __init__(self, parent, story_engine: StoryUniverseEngine, action_callback: Callable[[str], None]):
        self.parent = parent
        self.story_engine = story_engine
        self.action_callback = action_callback
        
        self.story_window = None
        self.current_tab = "character"
        
        # Story Engine Callbacks registrieren
        self._register_story_callbacks()
        
        logger.info("🎮 Story Universe GUI initialisiert")
    
    def _register_story_callbacks(self):
        """Registriert Story Engine Callbacks"""
        self.story_engine.register_story_callback("level_up", self._on_level_up)
        self.story_engine.register_story_callback("quest_completed", self._on_quest_completed)
        self.story_engine.register_story_callback("item_received", self._on_item_received)
        self.story_engine.register_story_callback("chapter_unlocked", self._on_chapter_unlocked)
        self.story_engine.register_story_callback("unlock_feature", self._on_feature_unlocked)
    
    def show_story_universe(self):
        """Zeigt das Story Universe Fenster"""
        if self.story_window and self.story_window.winfo_exists():
            self.story_window.lift()
            return
        
        self.story_window = tk.Toplevel(self.parent)
        self.story_window.title("🎮 Toobix Story Universe")
        self.story_window.geometry("1200x800")
        self.story_window.resizable(True, True)
        
        self._create_story_interface()
        self._update_all_displays()
    
    def show(self):
        """Alias für show_story_universe für bessere API Kompatibilität"""
        self.show_story_universe()
    
    def _create_story_interface(self):
        """Erstellt die Story-Benutzeroberfläche"""
        # Header mit Character-Info
        self._create_header()
        
        # Main Notebook für verschiedene Story-Bereiche
        if CTK_AVAILABLE:
            self.story_notebook = ctk.CTkTabview(self.story_window)
        else:
            self.story_notebook = ttk.Notebook(self.story_window)
        
        self.story_notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tabs erstellen
        self._create_character_tab()
        self._create_quests_tab()
        self._create_inventory_tab()
        self._create_chapters_tab()
        self._create_story_mode_tab()
        
        # Footer mit Actions
        self._create_footer()
    
    def _create_header(self):
        """Erstellt den Header mit Character-Info"""
        header_frame = ttk.Frame(self.story_window)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="🎮 Story Universe",
            font=("Arial", 16, "bold")
        )
        title_label.pack(side="left")
        
        # Quick Character Stats
        self.quick_stats_frame = ttk.Frame(header_frame)
        self.quick_stats_frame.pack(side="right")
        
        self.quick_stats_label = ttk.Label(
            self.quick_stats_frame,
            text="Lade Character...",
            font=("Arial", 10)
        )
        self.quick_stats_label.pack()
    
    def _create_character_tab(self):
        """Erstellt den Character-Tab"""
        if CTK_AVAILABLE:
            char_frame = self.story_notebook.add("👤 Character")
        else:
            char_frame = ttk.Frame(self.story_notebook)
            self.story_notebook.add(char_frame, text="👤 Character")
        
        # Character Portrait & Basic Info
        portrait_frame = ttk.LabelFrame(char_frame, text="Character Info", padding=10)
        portrait_frame.pack(fill="x", padx=10, pady=5)
        
        # Character Details
        details_frame = ttk.Frame(portrait_frame)
        details_frame.pack(fill="x")
        
        # Left: Avatar & Basic Info
        left_frame = ttk.Frame(details_frame)
        left_frame.pack(side="left", fill="y", padx=(0, 20))
        
        self.avatar_label = ttk.Label(left_frame, text="🧙‍♂️", font=("Arial", 48))
        self.avatar_label.pack()
        
        self.name_label = ttk.Label(left_frame, text="Character Name", font=("Arial", 14, "bold"))
        self.name_label.pack(pady=5)
        
        self.level_label = ttk.Label(left_frame, text="Level 1", font=("Arial", 12))
        self.level_label.pack()
        
        # Right: Stats & Progress
        right_frame = ttk.Frame(details_frame)
        right_frame.pack(side="left", fill="both", expand=True)
        
        # Experience Bar
        exp_frame = ttk.Frame(right_frame)
        exp_frame.pack(fill="x", pady=5)
        
        ttk.Label(exp_frame, text="Experience:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.exp_progress = ttk.Progressbar(exp_frame, mode="determinate")
        self.exp_progress.pack(fill="x", pady=2)
        self.exp_label = ttk.Label(exp_frame, text="0 / 100 XP", font=("Arial", 9))
        self.exp_label.pack(anchor="w")
        
        # Health & Energy
        vitals_frame = ttk.Frame(right_frame)
        vitals_frame.pack(fill="x", pady=5)
        
        health_frame = ttk.Frame(vitals_frame)
        health_frame.pack(fill="x")
        ttk.Label(health_frame, text="Health:", font=("Arial", 10, "bold")).pack(side="left")
        self.health_progress = ttk.Progressbar(health_frame, mode="determinate", length=150)
        self.health_progress.pack(side="left", padx=(5, 10))
        self.health_label = ttk.Label(health_frame, text="100/100", font=("Arial", 9))
        self.health_label.pack(side="left")
        
        energy_frame = ttk.Frame(vitals_frame)
        energy_frame.pack(fill="x", pady=2)
        ttk.Label(energy_frame, text="Energy:", font=("Arial", 10, "bold")).pack(side="left")
        self.energy_progress = ttk.Progressbar(energy_frame, mode="determinate", length=150)
        self.energy_progress.pack(side="left", padx=(5, 10))
        self.energy_label = ttk.Label(energy_frame, text="100/100", font=("Arial", 9))
        self.energy_label.pack(side="left")
        
        # Skills Section
        skills_frame = ttk.LabelFrame(char_frame, text="Skills & Abilities", padding=10)
        skills_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.skills_display = tk.Text(skills_frame, height=8, wrap="word", font=("Arial", 10))
        skills_scrollbar = ttk.Scrollbar(skills_frame, orient="vertical", command=self.skills_display.yview)
        self.skills_display.configure(yscrollcommand=skills_scrollbar.set)
        
        self.skills_display.pack(side="left", fill="both", expand=True)
        skills_scrollbar.pack(side="right", fill="y")
        
        # Achievements Section
        achievements_frame = ttk.LabelFrame(char_frame, text="Achievements", padding=10)
        achievements_frame.pack(fill="x", padx=10, pady=5)
        
        self.achievements_display = tk.Text(achievements_frame, height=4, wrap="word", font=("Arial", 9))
        self.achievements_display.pack(fill="x")
    
    def _create_quests_tab(self):
        """Erstellt den Quests-Tab"""
        if CTK_AVAILABLE:
            quest_frame = self.story_notebook.add("⚔️ Quests")
        else:
            quest_frame = ttk.Frame(self.story_notebook)
            self.story_notebook.add(quest_frame, text="⚔️ Quests")
        
        # Available Quests
        available_frame = ttk.LabelFrame(quest_frame, text="Available Quests", padding=10)
        available_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Quest List
        quest_list_frame = ttk.Frame(available_frame)
        quest_list_frame.pack(fill="both", expand=True)
        
        self.quest_listbox = tk.Listbox(quest_list_frame, height=6, font=("Arial", 10))
        quest_list_scrollbar = ttk.Scrollbar(quest_list_frame, orient="vertical", command=self.quest_listbox.yview)
        self.quest_listbox.configure(yscrollcommand=quest_list_scrollbar.set)
        
        self.quest_listbox.pack(side="left", fill="both", expand=True)
        quest_list_scrollbar.pack(side="right", fill="y")
        
        self.quest_listbox.bind("<<ListboxSelect>>", self._on_quest_select)
        
        # Quest Details
        quest_details_frame = ttk.LabelFrame(quest_frame, text="Quest Details", padding=10)
        quest_details_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.quest_details_display = tk.Text(quest_details_frame, height=8, wrap="word", font=("Arial", 10))
        quest_details_scrollbar = ttk.Scrollbar(quest_details_frame, orient="vertical", command=self.quest_details_display.yview)
        self.quest_details_display.configure(yscrollcommand=quest_details_scrollbar.set)
        
        self.quest_details_display.pack(side="left", fill="both", expand=True)
        quest_details_scrollbar.pack(side="right", fill="y")
        
        # Quest Actions
        quest_actions_frame = ttk.Frame(quest_frame)
        quest_actions_frame.pack(fill="x", padx=10, pady=5)
        
        self.start_quest_btn = ttk.Button(quest_actions_frame, text="🚀 Start Quest", command=self._start_selected_quest)
        self.start_quest_btn.pack(side="left", padx=5)
        
        self.complete_quest_btn = ttk.Button(quest_actions_frame, text="✅ Complete Quest", command=self._complete_selected_quest)
        self.complete_quest_btn.pack(side="left", padx=5)
    
    def _create_inventory_tab(self):
        """Erstellt den Inventory-Tab"""
        if CTK_AVAILABLE:
            inv_frame = self.story_notebook.add("🎒 Inventory")
        else:
            inv_frame = ttk.Frame(self.story_notebook)
            self.story_notebook.add(inv_frame, text="🎒 Inventory")
        
        # Inventory Grid
        inventory_frame = ttk.LabelFrame(inv_frame, text="Items", padding=10)
        inventory_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Items Canvas für Scrolling
        canvas_frame = ttk.Frame(inventory_frame)
        canvas_frame.pack(fill="both", expand=True)
        
        self.inventory_canvas = tk.Canvas(canvas_frame)
        inv_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.inventory_canvas.yview)
        self.inventory_frame = ttk.Frame(self.inventory_canvas)
        
        self.inventory_canvas.configure(yscrollcommand=inv_scrollbar.set)
        self.inventory_canvas.create_window((0, 0), window=self.inventory_frame, anchor="nw")
        
        self.inventory_canvas.pack(side="left", fill="both", expand=True)
        inv_scrollbar.pack(side="right", fill="y")
        
        # Update scroll region
        def _on_inventory_configure(event):
            self.inventory_canvas.configure(scrollregion=self.inventory_canvas.bbox("all"))
        self.inventory_frame.bind("<Configure>", _on_inventory_configure)
        
        # Item Details
        item_details_frame = ttk.LabelFrame(inv_frame, text="Item Details", padding=10)
        item_details_frame.pack(fill="x", padx=10, pady=5)
        
        self.item_details_display = tk.Text(item_details_frame, height=6, wrap="word", font=("Arial", 10))
        self.item_details_display.pack(fill="x")
        
        # Item Actions
        item_actions_frame = ttk.Frame(inv_frame)
        item_actions_frame.pack(fill="x", padx=10, pady=5)
        
        self.use_item_btn = ttk.Button(item_actions_frame, text="🔥 Use Item", command=self._use_selected_item)
        self.use_item_btn.pack(side="left", padx=5)
        
        self.selected_item = None
    
    def _create_chapters_tab(self):
        """Erstellt den Chapters-Tab"""
        if CTK_AVAILABLE:
            chapters_frame = self.story_notebook.add("📚 Chapters")
        else:
            chapters_frame = ttk.Frame(self.story_notebook)
            self.story_notebook.add(chapters_frame, text="📚 Chapters")
        
        # Chapter List
        chapter_list_frame = ttk.LabelFrame(chapters_frame, text="Story Chapters", padding=10)
        chapter_list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.chapters_listbox = tk.Listbox(chapter_list_frame, height=6, font=("Arial", 10))
        chapters_scrollbar = ttk.Scrollbar(chapter_list_frame, orient="vertical", command=self.chapters_listbox.yview)
        self.chapters_listbox.configure(yscrollcommand=chapters_scrollbar.set)
        
        self.chapters_listbox.pack(side="left", fill="both", expand=True)
        chapters_scrollbar.pack(side="right", fill="y")
        
        self.chapters_listbox.bind("<<ListboxSelect>>", self._on_chapter_select)
        
        # Chapter Details
        chapter_details_frame = ttk.LabelFrame(chapters_frame, text="Chapter Details", padding=10)
        chapter_details_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.chapter_details_display = tk.Text(chapter_details_frame, height=8, wrap="word", font=("Arial", 10))
        chapter_details_scrollbar = ttk.Scrollbar(chapter_details_frame, orient="vertical", command=self.chapter_details_display.yview)
        self.chapter_details_display.configure(yscrollcommand=chapter_details_scrollbar.set)
        
        self.chapter_details_display.pack(side="left", fill="both", expand=True)
        chapter_details_scrollbar.pack(side="right", fill="y")
    
    def _create_story_mode_tab(self):
        """Erstellt den Story Mode Tab"""
        if CTK_AVAILABLE:
            story_frame = self.story_notebook.add("🎭 Story Mode")
        else:
            story_frame = ttk.Frame(self.story_notebook)
            self.story_notebook.add(story_frame, text="🎭 Story Mode")
        
        # Story Mode Controls
        controls_frame = ttk.LabelFrame(story_frame, text="Story Mode Controls", padding=10)
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        control_buttons_frame = ttk.Frame(controls_frame)
        control_buttons_frame.pack(fill="x")
        
        self.start_story_btn = ttk.Button(control_buttons_frame, text="🎬 Start Story Mode", command=self._start_story_mode)
        self.start_story_btn.pack(side="left", padx=5)
        
        self.stop_story_btn = ttk.Button(control_buttons_frame, text="⏹️ Stop Story Mode", command=self._stop_story_mode)
        self.stop_story_btn.pack(side="left", padx=5)
        
        # Story Display
        story_display_frame = ttk.LabelFrame(story_frame, text="Interactive Story", padding=10)
        story_display_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.story_display = tk.Text(story_display_frame, wrap="word", font=("Arial", 11))
        story_display_scrollbar = ttk.Scrollbar(story_display_frame, orient="vertical", command=self.story_display.yview)
        self.story_display.configure(yscrollcommand=story_display_scrollbar.set)
        
        self.story_display.pack(side="left", fill="both", expand=True)
        story_display_scrollbar.pack(side="right", fill="y")
        
        # Story Choices
        choices_frame = ttk.Frame(story_frame)
        choices_frame.pack(fill="x", padx=10, pady=5)
        
        self.choice_buttons = []
    
    def _create_footer(self):
        """Erstellt den Footer mit Actions"""
        footer_frame = ttk.Frame(self.story_window)
        footer_frame.pack(fill="x", padx=10, pady=5)
        
        # Status
        self.status_label = ttk.Label(footer_frame, text="Story Universe bereit...")
        self.status_label.pack(side="left")
        
        # Actions
        ttk.Button(footer_frame, text="🔄 Refresh", command=self._update_all_displays).pack(side="right", padx=5)
        ttk.Button(footer_frame, text="💾 Save Progress", command=self._save_progress).pack(side="right", padx=5)
        ttk.Button(footer_frame, text="❌ Close", command=self.story_window.destroy).pack(side="right", padx=5)
    
    def _update_all_displays(self):
        """Aktualisiert alle Display-Elemente"""
        self._update_character_display()
        self._update_quests_display()
        self._update_inventory_display()
        self._update_chapters_display()
        self._update_quick_stats()
    
    def _update_character_display(self):
        """Aktualisiert Character-Anzeige"""
        if not hasattr(self, 'name_label'):
            return
        
        char_status = self.story_engine.get_character_status()
        if not char_status:
            return
        
        # Basic Info
        self.name_label.config(text=char_status["name"])
        self.level_label.config(text=f"Level {char_status['level']}")
        
        # Experience Bar
        current_exp = char_status["experience"]
        next_level_exp = char_status["next_level_exp"]
        exp_progress = (current_exp % 100) / 100 * 100  # Vereinfacht für Demo
        
        self.exp_progress.config(value=exp_progress)
        self.exp_label.config(text=f"{current_exp} / {int(next_level_exp)} XP")
        
        # Health & Energy
        self.health_progress.config(value=char_status["health"])
        self.health_label.config(text=f"{char_status['health']}/100")
        
        self.energy_progress.config(value=char_status["energy"])
        self.energy_label.config(text=f"{char_status['energy']}/100")
        
        # Skills
        self.skills_display.config(state="normal")
        self.skills_display.delete("1.0", tk.END)
        
        skills_text = "🎯 CHARACTER SKILLS:\n\n"
        for skill, level in char_status["skills"].items():
            skills_text += f"📊 {skill.title()}: Level {level}\n"
        
        skills_text += f"\n📈 STATISTICS:\n"
        skills_text += f"🎒 Inventory Items: {char_status['inventory_count']}\n"
        skills_text += f"🏆 Achievements: {char_status['achievements_count']}\n"
        skills_text += f"📖 Current Chapter: {char_status['current_chapter'].title()}\n"
        
        self.skills_display.insert("1.0", skills_text)
        self.skills_display.config(state="disabled")
        
        # Achievements (vereinfacht)
        self.achievements_display.config(state="normal")
        self.achievements_display.delete("1.0", tk.END)
        self.achievements_display.insert("1.0", f"🏆 {char_status['achievements_count']} Achievements unlocked!\nContinue your journey to unlock more...")
        self.achievements_display.config(state="disabled")
    
    def _update_quests_display(self):
        """Aktualisiert Quest-Anzeige"""
        if not hasattr(self, 'quest_listbox'):
            return
        
        # Clear current list
        self.quest_listbox.delete(0, tk.END)
        
        # Add available quests
        available_quests = self.story_engine.get_available_quests()
        for quest in available_quests:
            display_text = f"⚔️ {quest.title} ({quest.difficulty})"
            self.quest_listbox.insert(tk.END, display_text)
    
    def _update_inventory_display(self):
        """Aktualisiert Inventory-Anzeige"""
        if not hasattr(self, 'inventory_frame'):
            return
        
        # Clear current items
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()
        
        # Add inventory items
        items = self.story_engine.get_inventory_items()
        
        row = 0
        col = 0
        for item in items:
            item_frame = ttk.Frame(self.inventory_frame, relief="raised", borderwidth=1)
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            # Item icon and name
            item_btn = ttk.Button(
                item_frame,
                text=f"{self._get_item_icon(item)} {item.name}",
                command=lambda i=item: self._select_item(i)
            )
            item_btn.pack(fill="x", padx=5, pady=5)
            
            # Rarity indicator
            rarity_label = ttk.Label(
                item_frame,
                text=item.rarity.title(),
                font=("Arial", 8),
                foreground=self._get_rarity_color(item.rarity)
            )
            rarity_label.pack(pady=(0, 5))
            
            col += 1
            if col >= 3:  # 3 columns
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(3):
            self.inventory_frame.grid_columnconfigure(i, weight=1)
    
    def _update_chapters_display(self):
        """Aktualisiert Chapters-Anzeige"""
        if not hasattr(self, 'chapters_listbox'):
            return
        
        # Clear current list
        self.chapters_listbox.delete(0, tk.END)
        
        # Add chapters
        chapters = self.story_engine.get_unlocked_chapters()
        for chapter in chapters:
            status = "🔓" if chapter.is_unlocked else "🔒"
            display_text = f"{status} {chapter.title}"
            self.chapters_listbox.insert(tk.END, display_text)
    
    def _update_quick_stats(self):
        """Aktualisiert Quick Stats im Header"""
        if not hasattr(self, 'quick_stats_label'):
            return
        
        char_status = self.story_engine.get_character_status()
        if char_status:
            stats_text = f"Level {char_status['level']} | XP: {char_status['experience']} | Energy: {char_status['energy']}/100"
            self.quick_stats_label.config(text=stats_text)
    
    def _get_item_icon(self, item: StoryItem) -> str:
        """Gibt Icon für Item-Typ zurück"""
        icons = {
            "tool": "🔧",
            "consumable": "🧪",
            "cosmetic": "✨",
            "unlock": "🗝️"
        }
        return icons.get(item.category, "📦")
    
    def _get_rarity_color(self, rarity: str) -> str:
        """Gibt Farbe für Seltenheit zurück"""
        colors = {
            "common": "gray",
            "rare": "blue", 
            "epic": "purple",
            "legendary": "orange"
        }
        return colors.get(rarity, "black")
    
    def _on_quest_select(self, event):
        """Behandelt Quest-Auswahl"""
        selection = self.quest_listbox.curselection()
        if not selection:
            return
        
        quests = self.story_engine.get_available_quests()
        if selection[0] < len(quests):
            quest = quests[selection[0]]
            self._show_quest_details(quest)
    
    def _show_quest_details(self, quest: StoryQuest):
        """Zeigt Quest-Details"""
        self.quest_details_display.config(state="normal")
        self.quest_details_display.delete("1.0", tk.END)
        
        details = f"""⚔️ {quest.title}

📖 BESCHREIBUNG:
{quest.description}

🎯 OBJECTIVES:
"""
        for i, objective in enumerate(quest.objectives, 1):
            details += f"{i}. {objective}\n"
        
        details += f"""
💰 REWARDS:
"""
        if "experience" in quest.rewards:
            details += f"• {quest.rewards['experience']} Experience Points\n"
        if "items" in quest.rewards:
            details += f"• Items: {', '.join(quest.rewards['items'])}\n"
        if "unlocks" in quest.rewards:
            details += f"• Unlocks: {', '.join(quest.rewards['unlocks'])}\n"
        
        details += f"""
⏱️ Estimated Time: {quest.estimated_time} minutes
🎭 Chapter: {quest.chapter.title()}
🔧 Toobix Integration: {quest.real_world_integration}
"""
        
        self.quest_details_display.insert("1.0", details)
        self.quest_details_display.config(state="disabled")
    
    def _on_chapter_select(self, event):
        """Behandelt Chapter-Auswahl"""
        selection = self.chapters_listbox.curselection()
        if not selection:
            return
        
        chapters = self.story_engine.get_unlocked_chapters()
        if selection[0] < len(chapters):
            chapter = chapters[selection[0]]
            self._show_chapter_details(chapter)
    
    def _show_chapter_details(self, chapter: StoryChapter):
        """Zeigt Chapter-Details"""
        self.chapter_details_display.config(state="normal")
        self.chapter_details_display.delete("1.0", tk.END)
        
        details = f"""📚 {chapter.title}

📖 DESCRIPTION:
{chapter.description}

📜 BACKGROUND STORY:
{chapter.background_story}

⚔️ QUESTS ({len(chapter.quests)}):
"""
        for quest_id in chapter.quests:
            if quest_id in self.story_engine.quests_database:
                quest = self.story_engine.quests_database[quest_id]
                status = "✅" if quest.is_completed else "📋"
                details += f"{status} {quest.title}\n"
        
        details += f"""
🔓 UNLOCKED FEATURES:
"""
        for feature in chapter.unlocked_features:
            details += f"• {feature.replace('_', ' ').title()}\n"
        
        details += f"""
📊 REQUIREMENTS:
• Minimum Level: {chapter.unlock_level}
• Status: {'🔓 Unlocked' if chapter.is_unlocked else '🔒 Locked'}
"""
        
        self.chapter_details_display.insert("1.0", details)
        self.chapter_details_display.config(state="disabled")
    
    def _select_item(self, item: StoryItem):
        """Wählt ein Item aus"""
        self.selected_item = item
        
        # Show item details
        self.item_details_display.config(state="normal")
        self.item_details_display.delete("1.0", tk.END)
        
        details = f"""{self._get_item_icon(item)} {item.name}

📖 DESCRIPTION:
{item.description}

✨ RARITY: {item.rarity.title()}
📂 CATEGORY: {item.category.title()}

🔥 EFFECTS:
"""
        for effect, value in item.effect.items():
            details += f"• {effect.replace('_', ' ').title()}: {value}\n"
        
        if item.unlock_condition:
            details += f"\n🔓 UNLOCK CONDITION:\n{item.unlock_condition}"
        
        self.item_details_display.insert("1.0", details)
        self.item_details_display.config(state="disabled")
    
    def _start_selected_quest(self):
        """Startet ausgewählte Quest"""
        selection = self.quest_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Quest Selected", "Please select a quest first.")
            return
        
        quests = self.story_engine.get_available_quests()
        if selection[0] < len(quests):
            quest = quests[selection[0]]
            
            # Quest in Chat-System starten
            self.action_callback(f"Starte Quest: {quest.title}")
            self.status_label.config(text=f"Quest gestartet: {quest.title}")
    
    def _complete_selected_quest(self):
        """Schließt ausgewählte Quest ab (für Demo/Testing)"""
        selection = self.quest_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Quest Selected", "Please select a quest first.")
            return
        
        quests = self.story_engine.get_available_quests()
        if selection[0] < len(quests):
            quest = quests[selection[0]]
            
            # Manually complete quest (for demo)
            self.story_engine._complete_quest(quest)
            self._update_all_displays()
            
            messagebox.showinfo("Quest Completed!", f"Quest '{quest.title}' completed!")
    
    def _use_selected_item(self):
        """Nutzt ausgewähltes Item"""
        if not self.selected_item:
            messagebox.showwarning("No Item Selected", "Please select an item first.")
            return
        
        # Use item
        self.story_engine._use_item(self.selected_item.id)
        self._update_all_displays()
        
        messagebox.showinfo("Item Used!", f"Used {self.selected_item.name}!")
    
    def _start_story_mode(self):
        """Startet Story Mode"""
        self.story_engine.start_story_mode()
        
        # Show story introduction
        self.story_display.config(state="normal")
        self.story_display.delete("1.0", tk.END)
        
        intro_text = """🎭 STORY MODE ACTIVATED

🌟 Welcome to the Toobix Story Universe! 🌟

You are about to embark on an epic journey where your real-world productivity 
actions in Toobix will shape your story character's destiny.

Every task you complete, every feature you master, and every goal you achieve 
will grant your character experience, unlock new abilities, and advance the story.

Your character awaits your commands...

What would you like to do first?
"""
        
        self.story_display.insert("1.0", intro_text)
        self.story_display.config(state="disabled")
        
        self.start_story_btn.config(state="disabled")
        self.stop_story_btn.config(state="normal")
        
        self.status_label.config(text="🎭 Story Mode Active - Your actions shape the story!")
    
    def _stop_story_mode(self):
        """Stoppt Story Mode"""
        self.story_engine.stop_story_mode()
        
        self.start_story_btn.config(state="normal")
        self.stop_story_btn.config(state="disabled")
        
        self.status_label.config(text="Story Mode deactivated")
    
    def _save_progress(self):
        """Speichert Fortschritt"""
        self.story_engine._save_data()
        messagebox.showinfo("Progress Saved", "Your story progress has been saved!")
    
    # Callback-Methoden für Story Events
    def _on_level_up(self, old_level: int, new_level: int):
        """Callback für Level-Up"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"🎉 LEVEL UP! {old_level} → {new_level}")
            self._update_all_displays()
    
    def _on_quest_completed(self, quest: StoryQuest):
        """Callback für Quest-Abschluss"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"✅ Quest completed: {quest.title}")
            self._update_all_displays()
    
    def _on_item_received(self, item: StoryItem):
        """Callback für Item-Erhalt"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"🎁 New item: {item.name}")
            self._update_all_displays()
    
    def _on_chapter_unlocked(self, chapter: StoryChapter):
        """Callback für Chapter-Freischaltung"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"📚 New chapter: {chapter.title}")
            self._update_all_displays()
    
    def _on_feature_unlocked(self, feature: str):
        """Callback für Feature-Freischaltung"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=f"🔓 Feature unlocked: {feature}")
