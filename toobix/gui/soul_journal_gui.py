"""
🌟 SOUL JOURNAL GUI
===================

Spirituelle Tagebuch-Interface mit:
- Tägliche Reflexions-Prompts
- AI-generierte Einsichten
- Dankbarkeits-Tracker
- Spirituelles Wachstums-Dashboard
- Vergebungsarbeit
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Dict, List, Any, Optional
import datetime

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

from .soul_journal_engine import SoulJournalEngine, get_soul_journal, initialize_soul_journal

class SoulJournalGUI:
    """
    📔 SOUL JOURNAL DASHBOARD
    
    Spirituelles Tagebuch für:
    - Tiefe Selbstreflexion
    - Dankbarkeits-Tracking
    - Vergebungsarbeit
    - Persönlichkeitswachstum
    - AI Wisdom Insights
    """
    
    def __init__(self, parent=None, ai_handler=None):
        self.parent = parent
        self.ai_handler = ai_handler
        self.window = None
        self.soul_journal = None
        
    def show(self, parent=None):
        """Zeigt das Soul Journal Dashboard"""
        if parent:
            self.parent = parent
            
        if self.window is None or not self.window.winfo_exists():
            self.create_window()
        else:
            self.window.lift()
            self.window.focus()
    
    def create_window(self):
        """Erstellt das Soul Journal Fenster"""
        self.window = ctk.CTkToplevel(self.parent) if CTK_AVAILABLE else tk.Toplevel(self.parent)
        self.window.title("📔 Soul Journal - Spirituelles Tagebuch")
        self.window.geometry("1200x800")
        
        # Initialisiere Soul Journal Engine
        self.soul_journal = get_soul_journal()
        if not self.soul_journal:
            self.soul_journal = initialize_soul_journal(self.ai_handler)
        
        self.setup_gui()
        
        # Cleanup beim Schließen
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        """Erstellt die GUI-Elemente"""
        
        # Header mit spirituellem Design
        self.create_header()
        
        # Main Container mit Notebook
        main_container = ctk.CTkFrame(self.window) if CTK_AVAILABLE else ttk.Frame(self.window)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Notebook für verschiedene Bereiche
        if CTK_AVAILABLE:
            self.notebook = ctk.CTkTabview(main_container)
        else:
            self.notebook = ttk.Notebook(main_container)
        
        self.notebook.pack(fill="both", expand=True)
        
        # Tabs erstellen
        self.create_daily_reflection_tab()
        self.create_gratitude_tracker_tab()
        self.create_growth_dashboard_tab()
        self.create_journal_history_tab()
        self.create_wisdom_insights_tab()
    
    def create_header(self):
        """Erstellt spirituellen Header"""
        header = ctk.CTkFrame(self.window) if CTK_AVAILABLE else ttk.Frame(self.window)
        header.pack(fill="x", padx=10, pady=5)
        
        # Titel mit spirituellem Symbol
        title = ctk.CTkLabel(
            header,
            text="📔 ✨ SOUL JOURNAL ✨ 🙏",
            font=ctk.CTkFont(size=24, weight="bold") if CTK_AVAILABLE else ("Arial", 20, "bold")
        ) if CTK_AVAILABLE else ttk.Label(header, text="📔 ✨ SOUL JOURNAL ✨ 🙏", font=("Arial", 20, "bold"))
        title.pack(pady=10)
        
        # Spiritueller Tagessegen
        blessing = self.get_daily_blessing()
        blessing_label = ctk.CTkLabel(
            header,
            text=blessing,
            font=ctk.CTkFont(size=14, style="italic") if CTK_AVAILABLE else ("Arial", 12, "italic"),
            text_color="#7B68EE" if CTK_AVAILABLE else None
        ) if CTK_AVAILABLE else ttk.Label(header, text=blessing, font=("Arial", 12, "italic"))
        blessing_label.pack(pady=(0, 5))
    
    def create_daily_reflection_tab(self):
        """Tab für tägliche Reflexionen"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("🌅 Daily Reflection")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="🌅 Daily Reflection")
        
        # Prompt Bereich
        prompt_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Heutige Reflexion")
        prompt_frame.pack(fill="x", padx=10, pady=5)
        
        # Prompt Generator
        prompt_controls = ctk.CTkFrame(prompt_frame) if CTK_AVAILABLE else ttk.Frame(prompt_frame)
        prompt_controls.pack(fill="x", padx=10, pady=5)
        
        # Kategorie-Auswahl
        category_label = ctk.CTkLabel(prompt_controls, text="Reflexions-Kategorie:") if CTK_AVAILABLE else ttk.Label(prompt_controls, text="Reflexions-Kategorie:")
        category_label.pack(side="left", padx=5)
        
        self.category_var = tk.StringVar(value="gratitude")
        categories = ["gratitude", "forgiveness", "love", "peace", "service", "wisdom"]
        category_menu = ctk.CTkOptionMenu(
            prompt_controls,
            values=categories,
            variable=self.category_var,
            command=self.update_prompt
        ) if CTK_AVAILABLE else ttk.Combobox(prompt_controls, textvariable=self.category_var, values=categories)
        category_menu.pack(side="left", padx=5)
        
        # Neuer Prompt Button
        new_prompt_btn = ctk.CTkButton(
            prompt_controls,
            text="✨ Neuer Prompt",
            command=self.generate_new_prompt
        ) if CTK_AVAILABLE else ttk.Button(prompt_controls, text="✨ Neuer Prompt", command=self.generate_new_prompt)
        new_prompt_btn.pack(side="left", padx=5)
        
        # Aktueller Prompt
        self.current_prompt = ctk.CTkLabel(
            prompt_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold") if CTK_AVAILABLE else ("Arial", 14, "bold"),
            wraplength=800,
            anchor="center"
        ) if CTK_AVAILABLE else ttk.Label(prompt_frame, text="", font=("Arial", 14, "bold"), wraplength=800, anchor="center")
        self.current_prompt.pack(pady=20, padx=20)
        
        # Reflexions-Eingabe
        reflection_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Deine Reflexion")
        reflection_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        reflection_label = ctk.CTkLabel(reflection_frame, text="💝 Teile deine Gedanken und Gefühle:") if CTK_AVAILABLE else ttk.Label(reflection_frame, text="💝 Teile deine Gedanken und Gefühle:")
        reflection_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.reflection_text = ctk.CTkTextbox(
            reflection_frame,
            height=200,
            font=ctk.CTkFont(size=12)
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(reflection_frame, height=10, font=("Arial", 11))
        self.reflection_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Submit Button
        submit_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.Frame(tab_frame)
        submit_frame.pack(fill="x", padx=10, pady=5)
        
        submit_btn = ctk.CTkButton(
            submit_frame,
            text="🙏 Reflexion speichern & AI-Insight erhalten",
            command=self.save_reflection,
            font=ctk.CTkFont(size=14, weight="bold") if CTK_AVAILABLE else ("Arial", 12, "bold")
        ) if CTK_AVAILABLE else ttk.Button(submit_frame, text="🙏 Reflexion speichern & AI-Insight erhalten", command=self.save_reflection)
        submit_btn.pack(pady=10)
        
        # AI Insight Bereich
        insight_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="AI Wisdom Insight")
        insight_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.ai_insight_text = ctk.CTkTextbox(
            insight_frame,
            height=150,
            font=ctk.CTkFont(size=12),
            text_color="#4A90E2" if CTK_AVAILABLE else None
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(insight_frame, height=8, font=("Arial", 11))
        self.ai_insight_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initialer Prompt
        self.generate_new_prompt()
    
    def create_gratitude_tracker_tab(self):
        """Tab für Dankbarkeits-Tracking"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("🙏 Gratitude")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="🙏 Gratitude")
        
        # Dankbarkeits-Counter
        counter_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Dankbarkeits-Zähler")
        counter_frame.pack(fill="x", padx=10, pady=5)
        
        # Tägliches Ziel
        goal_frame = ctk.CTkFrame(counter_frame) if CTK_AVAILABLE else ttk.Frame(counter_frame)
        goal_frame.pack(fill="x", padx=10, pady=10)
        
        self.gratitude_progress = ctk.CTkProgressBar(
            goal_frame,
            width=400,
            height=20
        ) if CTK_AVAILABLE else ttk.Progressbar(goal_frame, length=400)
        self.gratitude_progress.pack(side="left", padx=10)
        
        self.gratitude_label = ctk.CTkLabel(
            goal_frame,
            text="0/10 Dankbarkeiten heute",
            font=ctk.CTkFont(size=14, weight="bold") if CTK_AVAILABLE else ("Arial", 12, "bold")
        ) if CTK_AVAILABLE else ttk.Label(goal_frame, text="0/10 Dankbarkeiten heute", font=("Arial", 12, "bold"))
        self.gratitude_label.pack(side="left", padx=10)
        
        # Streak Info
        self.streak_label = ctk.CTkLabel(
            counter_frame,
            text="🔥 Streak: 0 Tage",
            font=ctk.CTkFont(size=12) if CTK_AVAILABLE else ("Arial", 10)
        ) if CTK_AVAILABLE else ttk.Label(counter_frame, text="🔥 Streak: 0 Tage", font=("Arial", 10))
        self.streak_label.pack(pady=5)
        
        # Schnelle Dankbarkeits-Eingabe
        quick_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Schnelle Dankbarkeit")
        quick_frame.pack(fill="x", padx=10, pady=5)
        
        quick_label = ctk.CTkLabel(quick_frame, text="💝 Wofür bist du gerade dankbar?") if CTK_AVAILABLE else ttk.Label(quick_frame, text="💝 Wofür bist du gerade dankbar?")
        quick_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        quick_input_frame = ctk.CTkFrame(quick_frame) if CTK_AVAILABLE else ttk.Frame(quick_frame)
        quick_input_frame.pack(fill="x", padx=10, pady=10)
        
        self.quick_gratitude_entry = ctk.CTkEntry(
            quick_input_frame,
            placeholder_text="z.B. Für diesen wunderschönen Sonnenaufgang...",
            font=ctk.CTkFont(size=12)
        ) if CTK_AVAILABLE else ttk.Entry(quick_input_frame, font=("Arial", 11))
        self.quick_gratitude_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.quick_gratitude_entry.bind("<Return>", lambda e: self.add_quick_gratitude())
        
        add_gratitude_btn = ctk.CTkButton(
            quick_input_frame,
            text="🙏 Hinzufügen",
            command=self.add_quick_gratitude,
            width=100
        ) if CTK_AVAILABLE else ttk.Button(quick_input_frame, text="🙏 Hinzufügen", command=self.add_quick_gratitude)
        add_gratitude_btn.pack(side="right")
        
        # Heutige Dankbarkeiten
        today_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Heutige Dankbarkeiten")
        today_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.today_gratitudes = ctk.CTkTextbox(
            today_frame,
            font=ctk.CTkFont(size=11)
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(today_frame, font=("Arial", 10))
        self.today_gratitudes.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.update_gratitude_display()
    
    def create_growth_dashboard_tab(self):
        """Tab für spirituelles Wachstum"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("🌱 Growth")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="🌱 Growth")
        
        # Wachstums-Kategorien
        categories_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Spirituelle Entwicklung")
        categories_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Growth Bars
        self.growth_bars = {}
        growth_categories = {
            'forgiveness': '🕊️ Vergebung',
            'compassion': '💝 Mitgefühl',
            'peace': '☮️ Frieden',
            'wisdom': '🌟 Weisheit',
            'love': '💖 Liebe',
            'gratitude': '🙏 Dankbarkeit',
            'service': '🤝 Dienst',
            'faith': '✨ Glaube'
        }
        
        for i, (category, display_name) in enumerate(growth_categories.items()):
            row = i // 2
            col = i % 2
            
            cat_frame = ctk.CTkFrame(categories_frame) if CTK_AVAILABLE else ttk.Frame(categories_frame)
            cat_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            
            label = ctk.CTkLabel(cat_frame, text=display_name, font=ctk.CTkFont(size=12, weight="bold") if CTK_AVAILABLE else ("Arial", 10, "bold")) if CTK_AVAILABLE else ttk.Label(cat_frame, text=display_name, font=("Arial", 10, "bold"))
            label.pack(anchor="w", padx=5, pady=(5, 0))
            
            progress = ctk.CTkProgressBar(cat_frame, width=250, height=15) if CTK_AVAILABLE else ttk.Progressbar(cat_frame, length=250)
            progress.pack(padx=5, pady=2)
            
            level_label = ctk.CTkLabel(cat_frame, text="Level 1.0", font=ctk.CTkFont(size=10) if CTK_AVAILABLE else ("Arial", 8)) if CTK_AVAILABLE else ttk.Label(cat_frame, text="Level 1.0", font=("Arial", 8))
            level_label.pack(anchor="w", padx=5, pady=(0, 5))
            
            self.growth_bars[category] = (progress, level_label)
        
        # Grid konfigurieren
        if hasattr(categories_frame, 'grid_columnconfigure'):
            categories_frame.grid_columnconfigure(0, weight=1)
            categories_frame.grid_columnconfigure(1, weight=1)
        
        self.update_growth_display()
    
    def create_journal_history_tab(self):
        """Tab für Journal-Historie"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("📚 History")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="📚 History")
        
        # Filteroptionen
        filter_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.Frame(tab_frame)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        filter_label = ctk.CTkLabel(filter_frame, text="Filter:") if CTK_AVAILABLE else ttk.Label(filter_frame, text="Filter:")
        filter_label.pack(side="left", padx=5)
        
        self.filter_var = tk.StringVar(value="all")
        filter_options = ["all", "gratitude", "forgiveness", "love", "peace", "service", "wisdom"]
        filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=filter_options,
            variable=self.filter_var,
            command=self.update_history_display
        ) if CTK_AVAILABLE else ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filter_options)
        filter_menu.pack(side="left", padx=5)
        
        # Geschichte anzeigen
        self.history_text = ctk.CTkTextbox(
            tab_frame,
            font=ctk.CTkFont(size=11)
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(tab_frame, font=("Arial", 10))
        self.history_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.update_history_display()
    
    def create_wisdom_insights_tab(self):
        """Tab für AI-Weisheits-Einsichten"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("🌟 Wisdom")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="🌟 Wisdom")
        
        # Persönliche Einsichten
        insights_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Persönliche Einsichten")
        insights_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.insights_text = ctk.CTkTextbox(
            insights_frame,
            font=ctk.CTkFont(size=12),
            text_color="#4A90E2" if CTK_AVAILABLE else None
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(insights_frame, font=("Arial", 11))
        self.insights_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Aktionsbuttons
        action_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.Frame(tab_frame)
        action_frame.pack(fill="x", padx=10, pady=5)
        
        generate_insights_btn = ctk.CTkButton(
            action_frame,
            text="✨ Neue Einsichten generieren",
            command=self.generate_wisdom_insights
        ) if CTK_AVAILABLE else ttk.Button(action_frame, text="✨ Neue Einsichten generieren", command=self.generate_wisdom_insights)
        generate_insights_btn.pack(side="left", padx=5)
        
        export_btn = ctk.CTkButton(
            action_frame,
            text="📤 Weisheiten exportieren",
            command=self.export_wisdom
        ) if CTK_AVAILABLE else ttk.Button(action_frame, text="📤 Weisheiten exportieren", command=self.export_wisdom)
        export_btn.pack(side="left", padx=5)
        
        self.generate_wisdom_insights()
    
    def get_daily_blessing(self) -> str:
        """Gibt einen täglichen spirituellen Segen zurück"""
        blessings = [
            "💝 Möge dein Herz heute von Liebe und Dankbarkeit erfüllt sein",
            "🌟 Mögest du heute Frieden in dir und um dich herum finden",
            "🙏 Möge jeder Moment ein Geschenk der Weisheit für dich sein",
            "✨ Mögest du heute ein Licht der Hoffnung für andere sein",
            "💚 Möge Vergebung dein Herz heilen und befreien",
            "🕊️ Mögest du heute in Harmonie mit allem Leben stehen",
            "🌱 Möge jede Herausforderung zu spirituellem Wachstum werden"
        ]
        import random
        return random.choice(blessings)
    
    def generate_new_prompt(self):
        """Generiert einen neuen Reflexions-Prompt"""
        if not self.soul_journal:
            return
        
        category = self.category_var.get()
        
        # Tageszeit bestimmen
        hour = datetime.datetime.now().hour
        if hour < 12:
            time_of_day = "morning"
        elif hour < 18:
            time_of_day = "midday"
        else:
            time_of_day = "evening"
        
        prompt = self.soul_journal.get_daily_prompt(time_of_day, category)
        self.current_prompt.configure(text=prompt)
    
    def update_prompt(self, *args):
        """Aktualisiert Prompt bei Kategorie-Änderung"""
        self.generate_new_prompt()
    
    def save_reflection(self):
        """Speichert Reflexion und generiert AI-Insight"""
        if not self.soul_journal:
            messagebox.showerror("Fehler", "Soul Journal System nicht verfügbar")
            return
        
        category = self.category_var.get()
        prompt = self.current_prompt.cget("text")
        reflection = self.reflection_text.get("1.0", "end-1c") if CTK_AVAILABLE else self.reflection_text.get("1.0", tk.END).strip()
        
        if not reflection.strip():
            messagebox.showwarning("Warnung", "Bitte schreibe eine Reflexion bevor du speicherst.")
            return
        
        try:
            # Entry erstellen
            entry = self.soul_journal.create_entry(category, prompt, reflection)
            
            # AI-Insight anzeigen
            self.ai_insight_text.delete("1.0", "end") if CTK_AVAILABLE else self.ai_insight_text.delete("1.0", tk.END)
            self.ai_insight_text.insert("1.0", entry.ai_insight)
            
            # Reflexions-Text leeren
            self.reflection_text.delete("1.0", "end") if CTK_AVAILABLE else self.reflection_text.delete("1.0", tk.END)
            
            # Displays aktualisieren
            self.update_gratitude_display()
            self.update_growth_display()
            self.update_history_display()
            
            messagebox.showinfo("Erfolg", "Reflexion gespeichert! 🙏✨")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")
    
    def add_quick_gratitude(self):
        """Fügt schnelle Dankbarkeit hinzu"""
        gratitude_text = self.quick_gratitude_entry.get().strip()
        
        if not gratitude_text:
            return
        
        if self.soul_journal:
            # Als Dankbarkeits-Entry speichern
            prompt = "💝 Schnelle Dankbarkeit"
            entry = self.soul_journal.create_entry("gratitude", prompt, gratitude_text)
            
            # Entry leeren
            self.quick_gratitude_entry.delete(0, "end") if CTK_AVAILABLE else self.quick_gratitude_entry.delete(0, tk.END)
            
            # Display aktualisieren
            self.update_gratitude_display()
            
            # Kurzes Feedback
            messagebox.showinfo("Dankbarkeit", f"🙏 Dankbarkeit hinzugefügt! ({self.soul_journal.gratitude_counter.current_count}/{self.soul_journal.gratitude_counter.daily_goal})")
    
    def update_gratitude_display(self):
        """Aktualisiert Dankbarkeits-Anzeige"""
        if not self.soul_journal:
            return
        
        counter = self.soul_journal.gratitude_counter
        
        # Progress Bar
        progress = min(1.0, counter.current_count / counter.daily_goal)
        if CTK_AVAILABLE:
            self.gratitude_progress.set(progress)
        else:
            self.gratitude_progress['value'] = progress * 100
        
        # Label
        self.gratitude_label.configure(text=f"{counter.current_count}/{counter.daily_goal} Dankbarkeiten heute")
        
        # Streak
        self.streak_label.configure(text=f"🔥 Streak: {counter.gratitude_streak} Tage")
        
        # Heutige Dankbarkeiten anzeigen
        today = datetime.date.today()
        today_entries = [
            entry for entry in self.soul_journal.entries
            if entry.category == "gratitude" and entry.timestamp.date() == today
        ]
        
        today_text = "🙏 HEUTIGE DANKBARKEITEN:\n\n"
        
        for i, entry in enumerate(today_entries, 1):
            time_str = entry.timestamp.strftime("%H:%M")
            today_text += f"{i}. [{time_str}] {entry.user_reflection}\n\n"
        
        if not today_entries:
            today_text += "Noch keine Dankbarkeiten heute. Wofür bist du dankbar? 💝"
        
        self.today_gratitudes.delete("1.0", "end") if CTK_AVAILABLE else self.today_gratitudes.delete("1.0", tk.END)
        self.today_gratitudes.insert("1.0", today_text)
    
    def update_growth_display(self):
        """Aktualisiert Wachstums-Anzeige"""
        if not self.soul_journal:
            return
        
        growth_data = self.soul_journal.growth_tracker.categories
        
        for category, (progress_bar, level_label) in self.growth_bars.items():
            level = growth_data.get(category, 1.0)
            
            # Progress (0-1 für Level 0-10)
            progress_value = min(1.0, level / 10.0)
            if CTK_AVAILABLE:
                progress_bar.set(progress_value)
            else:
                progress_bar['value'] = progress_value * 100
            
            # Level anzeigen
            level_label.configure(text=f"Level {level:.1f}/10")
    
    def update_history_display(self, *args):
        """Aktualisiert Historie-Anzeige"""
        if not self.soul_journal:
            return
        
        filter_category = self.filter_var.get()
        
        # Einträge filtern
        if filter_category == "all":
            entries = self.soul_journal.entries
        else:
            entries = [e for e in self.soul_journal.entries if e.category == filter_category]
        
        # Sortiere nach Datum (neueste zuerst)
        entries = sorted(entries, key=lambda e: e.timestamp, reverse=True)
        
        # Historie-Text erstellen
        history_text = f"📚 JOURNAL HISTORIE ({len(entries)} Einträge)\n\n"
        
        for entry in entries[:20]:  # Zeige nur die letzten 20
            date_str = entry.timestamp.strftime("%d.%m.%Y %H:%M")
            category_emoji = {
                'gratitude': '🙏',
                'forgiveness': '🕊️',
                'love': '💖',
                'peace': '☮️',
                'service': '🤝',
                'wisdom': '🌟'
            }.get(entry.category, '📝')
            
            history_text += f"{category_emoji} [{date_str}] {entry.category.upper()}\n"
            history_text += f"💭 {entry.user_reflection[:100]}{'...' if len(entry.user_reflection) > 100 else ''}\n"
            history_text += f"✨ Tiefe: {entry.emotional_depth:.2f} | Wachstum: {entry.spiritual_growth:.3f}\n"
            history_text += "-" * 50 + "\n\n"
        
        self.history_text.delete("1.0", "end") if CTK_AVAILABLE else self.history_text.delete("1.0", tk.END)
        self.history_text.insert("1.0", history_text)
    
    def generate_wisdom_insights(self):
        """Generiert persönliche Weisheits-Einsichten"""
        if not self.soul_journal:
            return
        
        growth_insights = self.soul_journal.get_growth_insights()
        
        insights_text = "🌟 PERSÖNLICHE WEISHEITS-EINSICHTEN\n\n"
        
        insights_text += f"📊 JOURNAL STATISTIKEN:\n"
        insights_text += f"• Total Einträge: {growth_insights.get('total_entries', 0)}\n"
        insights_text += f"• Durchschnittliche Tiefe: {growth_insights.get('recent_avg_depth', 0):.2f}\n"
        insights_text += f"• Spirituelles Wachstum: {growth_insights.get('recent_avg_growth', 0):.3f}\n"
        insights_text += f"• Stärkster Bereich: {growth_insights.get('strongest_growth_area', 'N/A')}\n"
        insights_text += f"• Dankbarkeits-Streak: {growth_insights.get('gratitude_streak', 0)} Tage\n\n"
        
        insights_text += f"🌱 WACHSTUMS-EINSICHTEN:\n"
        
        # Analysiere Wachstumsmuster
        if growth_insights.get('total_entries', 0) > 0:
            if growth_insights.get('recent_avg_depth', 0) > 0.7:
                insights_text += "• 💫 Du gehst sehr tief in deine Reflexionen - das zeigt spirituelle Reife\n"
            
            if growth_insights.get('gratitude_streak', 0) > 7:
                insights_text += "• 🙏 Deine Dankbarkeits-Praxis ist beeindruckend konstant!\n"
            
            strongest = growth_insights.get('strongest_growth_area', '')
            if strongest == 'forgiveness':
                insights_text += "• 🕊️ Vergebung ist deine Superkraft - du transformierst Schmerz in Weisheit\n"
            elif strongest == 'love':
                insights_text += "• 💖 Deine Fähigkeit zu lieben wächst exponentiell - du wirst zum Lichtträger\n"
            elif strongest == 'gratitude':
                insights_text += "• 🙏 Dankbarkeit öffnet dein Herz für immer größere Segnungen\n"
        else:
            insights_text += "• 🌱 Beginne deine spirituelle Reise - jeder Schritt zählt!\n"
        
        insights_text += f"\n✨ SPIRITUELLE EMPFEHLUNGEN:\n"
        insights_text += "• 🧘 Täglich 5 Minuten Meditation für inneren Frieden\n"
        insights_text += "• 💝 3 Dankbarkeiten vor dem Schlafengehen\n"
        insights_text += "• 🕊️ Vergebungsarbeit bei alten Verletzungen\n"
        insights_text += "• 🤝 Ein Akt der Güte täglich für spirituelles Wachstum\n"
        
        self.insights_text.delete("1.0", "end") if CTK_AVAILABLE else self.insights_text.delete("1.0", tk.END)
        self.insights_text.insert("1.0", insights_text)
    
    def export_wisdom(self):
        """Exportiert Weisheiten und Einsichten"""
        if not self.soul_journal:
            return
        
        try:
            # Exportiere als Text-Datei
            export_text = "🌟 SOUL JOURNAL EXPORT\n"
            export_text += f"Exportiert am: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            export_text += "=" * 50 + "\n\n"
            
            # Alle Einträge
            for entry in sorted(self.soul_journal.entries, key=lambda e: e.timestamp):
                export_text += f"📅 {entry.timestamp.strftime('%d.%m.%Y %H:%M')} - {entry.category.upper()}\n"
                export_text += f"💭 PROMPT: {entry.prompt}\n"
                export_text += f"📝 REFLEXION: {entry.user_reflection}\n"
                export_text += f"✨ AI-INSIGHT: {entry.ai_insight}\n"
                export_text += f"📊 Tiefe: {entry.emotional_depth:.2f} | Wachstum: {entry.spiritual_growth:.3f}\n"
                export_text += "-" * 50 + "\n\n"
            
            # Datei speichern Dialog
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Soul Journal exportieren"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(export_text)
                
                messagebox.showinfo("Export erfolgreich", f"Soul Journal exportiert nach:\n{filename}")
        
        except Exception as e:
            messagebox.showerror("Export Fehler", f"Fehler beim Exportieren: {e}")
    
    def on_closing(self):
        """Cleanup beim Schließen"""
        if self.window:
            self.window.destroy()
            self.window = None

# Globale Instanz
soul_journal_gui = None

def show_soul_journal(parent=None, ai_handler=None):
    """Zeigt das Soul Journal Dashboard"""
    global soul_journal_gui
    
    if soul_journal_gui is None:
        soul_journal_gui = SoulJournalGUI(parent, ai_handler)
    
    soul_journal_gui.show(parent)
    return soul_journal_gui
