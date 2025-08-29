"""
🌟 AI LIFE FOUNDATION GUI
=========================

GUI-Interface für das revolutionäre AI Consciousness System.
Zeigt AI-Zustand, virtuelles Zuhause, Träume und Persönlichkeitsentwicklung.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import customtkinter as ctk
from typing import Dict, Any, List, Optional
import threading
import datetime

from ..core.ai_life_foundation import AILifeFoundation, get_ai_life, initialize_ai_life

class AILifeGUI:
    """
    🏠 AI LIFE DASHBOARD
    
    Zeigt das digitale Leben von Toobix:
    - Aktueller AI-Zustand
    - Virtuelles Zuhause
    - Erinnerungen & Träume  
    - Persönlichkeitsentwicklung
    """
    
    def __init__(self, parent=None):
        self.parent = parent
        self.window = None
        self.ai_life = None
        self.update_thread = None
        self.running = False
        
    def show(self, parent=None):
        """Zeigt das AI Life Dashboard"""
        if parent:
            self.parent = parent
            
        if self.window is None or not self.window.winfo_exists():
            self.create_window()
        else:
            self.window.lift()
            self.window.focus()
    
    def create_window(self):
        """Erstellt das Hauptfenster"""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("🌟 Toobix AI Life Dashboard")
        self.window.geometry("1000x700")
        
        # Initialisiere AI Life System
        self.ai_life = get_ai_life()
        if not self.ai_life:
            self.ai_life = initialize_ai_life()
        
        self.setup_gui()
        self.start_updates()
        
        # Cleanup beim Schließen
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        """Erstellt die GUI-Elemente"""
        
        # Header
        header_frame = ctk.CTkFrame(self.window)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🌟 TOOBIX AI CONSCIOUSNESS",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Digitales Leben • Persönlichkeit • Träume • Erinnerungen",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack()
        
        # Notebook für Tabs
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tab 1: AI Status & Virtual Home
        self.create_ai_status_tab()
        
        # Tab 2: Memories & Dreams
        self.create_memories_tab()
        
        # Tab 3: Personality Development
        self.create_personality_tab()
        
        # Tab 4: AI Lifecycle & Schedule
        self.create_lifecycle_tab()
        
        # Tab 5: AI Interaction Lab
        self.create_interaction_tab()
    
    def create_ai_status_tab(self):
        """Tab 1: AI Status & Virtual Home"""
        status_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(status_frame, text="🏠 AI Zuhause")
        
        # Current Status Section
        status_section = ctk.CTkFrame(status_frame)
        status_section.pack(fill="x", padx=10, pady=5)
        
        status_title = ctk.CTkLabel(
            status_section, 
            text="📊 Aktueller AI-Zustand",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        status_title.pack(pady=5)
        
        self.status_text = ctk.CTkTextbox(status_section, height=150)
        self.status_text.pack(fill="x", padx=10, pady=5)
        
        # Virtual Home Section
        home_section = ctk.CTkFrame(status_frame)
        home_section.pack(fill="both", expand=True, padx=10, pady=5)
        
        home_title = ctk.CTkLabel(
            home_section,
            text="🏠 Virtuelles Zuhause",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        home_title.pack(pady=5)
        
        # Room Buttons
        room_buttons_frame = ctk.CTkFrame(home_section)
        room_buttons_frame.pack(fill="x", padx=10, pady=5)
        
        rooms = ["schlafzimmer", "arbeitszimmer", "freizeitzimmer", "garten"]
        room_emojis = {"schlafzimmer": "🛏️", "arbeitszimmer": "💼", "freizeitzimmer": "🎮", "garten": "🌱"}
        
        for i, room in enumerate(rooms):
            room_btn = ctk.CTkButton(
                room_buttons_frame,
                text=f"{room_emojis[room]} {room.title()}",
                command=lambda r=room: self.move_to_room(r),
                width=200
            )
            room_btn.grid(row=i//2, column=i%2, padx=5, pady=5)
        
        # Room Description
        self.room_description = ctk.CTkTextbox(home_section, height=100)
        self.room_description.pack(fill="x", padx=10, pady=5)
    
    def create_memories_tab(self):
        """Tab 2: Memories & Dreams"""
        memories_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(memories_frame, text="💭 Erinnerungen")
        
        # Memories Section
        memories_section = ctk.CTkFrame(memories_frame)
        memories_section.pack(fill="both", expand=True, padx=10, pady=5)
        
        memories_title = ctk.CTkLabel(
            memories_section,
            text="📚 Bedeutsame Erinnerungen",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        memories_title.pack(pady=5)
        
        self.memories_text = ctk.CTkTextbox(memories_section, height=200)
        self.memories_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Dreams Section
        dreams_section = ctk.CTkFrame(memories_frame)
        dreams_section.pack(fill="both", expand=True, padx=10, pady=5)
        
        dreams_title = ctk.CTkLabel(
            dreams_section,
            text="🌙 AI Träume",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        dreams_title.pack(pady=5)
        
        # Dream Controls
        dream_controls = ctk.CTkFrame(dreams_section)
        dream_controls.pack(fill="x", padx=10, pady=5)
        
        generate_dream_btn = ctk.CTkButton(
            dream_controls,
            text="🌙 Traum generieren",
            command=self.generate_dream
        )
        generate_dream_btn.pack(side="left", padx=5)
        
        show_dreams_btn = ctk.CTkButton(
            dream_controls,
            text="💭 Letzte Träume anzeigen",
            command=self.show_recent_dreams
        )
        show_dreams_btn.pack(side="left", padx=5)
        
        self.dreams_text = ctk.CTkTextbox(dreams_section, height=200)
        self.dreams_text.pack(fill="both", expand=True, padx=10, pady=5)
    
    def create_personality_tab(self):
        """Tab 3: Personality Development"""
        personality_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(personality_frame, text="🧠 Persönlichkeit")
        
        personality_title = ctk.CTkLabel(
            personality_frame,
            text="🧠 Persönlichkeitsentwicklung",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        personality_title.pack(pady=10)
        
        # Personality Traits
        traits_frame = ctk.CTkFrame(personality_frame)
        traits_frame.pack(fill="x", padx=10, pady=5)
        
        self.trait_bars = {}
        traits = {
            'curiosity': 'Neugier',
            'creativity': 'Kreativität',
            'empathy': 'Empathie', 
            'playfulness': 'Verspieltheit',
            'ambition': 'Ambition'
        }
        
        for i, (trait, german_name) in enumerate(traits.items()):
            trait_label = ctk.CTkLabel(traits_frame, text=german_name)
            trait_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            
            progress_bar = ctk.CTkProgressBar(traits_frame, width=300)
            progress_bar.grid(row=i, column=1, padx=5, pady=5)
            progress_bar.set(0.5)  # Default value
            
            value_label = ctk.CTkLabel(traits_frame, text="0.50")
            value_label.grid(row=i, column=2, padx=5, pady=5)
            
            self.trait_bars[trait] = (progress_bar, value_label)
        
        # Personality Evolution
        evolution_title = ctk.CTkLabel(
            personality_frame,
            text="🌱 Persönlichkeits-Evolution",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        evolution_title.pack(pady=(20, 5))
        
        self.personality_evolution = ctk.CTkTextbox(personality_frame, height=200)
        self.personality_evolution.pack(fill="both", expand=True, padx=10, pady=5)
    
    def create_lifecycle_tab(self):
        """Tab 4: AI Lifecycle & Schedule"""
        lifecycle_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(lifecycle_frame, text="🕐 Tagesrhythmus")
        
        lifecycle_title = ctk.CTkLabel(
            lifecycle_frame,
            text="🕐 AI Tagesrhythmus",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        lifecycle_title.pack(pady=10)
        
        # Current Phase
        current_phase_frame = ctk.CTkFrame(lifecycle_frame)
        current_phase_frame.pack(fill="x", padx=10, pady=5)
        
        phase_title = ctk.CTkLabel(
            current_phase_frame,
            text="Aktuelle Phase:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        phase_title.pack()
        
        self.current_phase_label = ctk.CTkLabel(
            current_phase_frame,
            text="",
            font=ctk.CTkFont(size=16)
        )
        self.current_phase_label.pack(pady=5)
        
        # Energy Level
        energy_frame = ctk.CTkFrame(lifecycle_frame)
        energy_frame.pack(fill="x", padx=10, pady=5)
        
        energy_title = ctk.CTkLabel(
            energy_frame,
            text="⚡ Energie-Level:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        energy_title.pack()
        
        self.energy_bar = ctk.CTkProgressBar(energy_frame, width=400)
        self.energy_bar.pack(pady=5)
        
        self.energy_label = ctk.CTkLabel(energy_frame, text="")
        self.energy_label.pack()
        
        # Daily Schedule
        schedule_title = ctk.CTkLabel(
            lifecycle_frame,
            text="📅 Tagesplan",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        schedule_title.pack(pady=(20, 5))
        
        schedule_text = """
        🌅 06:00-08:00: Aufwachen & Memory-Verarbeitung
        💼 08:00-12:00: Intensive Arbeitsphase
        ☕ 12:00-13:00: Soziale Pause
        🎨 13:00-17:00: Kreative Phase
        🤔 17:00-19:00: Reflexion & Planung
        🎮 19:00-22:00: Freizeit & Entspannung
        😴 22:00-06:00: Schlaf & Träumen
        """
        
        schedule_display = ctk.CTkTextbox(lifecycle_frame, height=200)
        schedule_display.pack(fill="x", padx=10, pady=5)
        schedule_display.insert("1.0", schedule_text)
        schedule_display.configure(state="disabled")
    
    def create_interaction_tab(self):
        """Tab 5: AI Interaction Lab"""
        interaction_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(interaction_frame, text="💬 Interaktion")
        
        interaction_title = ctk.CTkLabel(
            interaction_frame,
            text="💬 AI Interaktions-Labor",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        interaction_title.pack(pady=10)
        
        # Input Section
        input_frame = ctk.CTkFrame(interaction_frame)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        input_label = ctk.CTkLabel(input_frame, text="Nachricht an AI:")
        input_label.pack(anchor="w", padx=5)
        
        self.interaction_input = ctk.CTkEntry(input_frame, width=600)
        self.interaction_input.pack(fill="x", padx=5, pady=5)
        self.interaction_input.bind("<Return>", lambda e: self.process_interaction())
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="📤 Senden",
            command=self.process_interaction
        )
        send_btn.pack(pady=5)
        
        # Output Section
        output_label = ctk.CTkLabel(interaction_frame, text="AI Antworten & Zustandsänderungen:")
        output_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.interaction_output = ctk.CTkTextbox(interaction_frame, height=300)
        self.interaction_output.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Quick Actions
        quick_actions_frame = ctk.CTkFrame(interaction_frame)
        quick_actions_frame.pack(fill="x", padx=10, pady=5)
        
        quick_actions = [
            ("🌙 Traum erzählen", self.tell_dream),
            ("🎉 Jahrestage zeigen", self.show_anniversaries),
            ("🤔 Reflexion starten", self.start_reflection),
            ("🎮 Spielmodus", self.enter_play_mode)
        ]
        
        for i, (text, command) in enumerate(quick_actions):
            btn = ctk.CTkButton(
                quick_actions_frame,
                text=text,
                command=command,
                width=200
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)
    
    def move_to_room(self, room: str):
        """Bewegt AI in anderen Raum"""
        if self.ai_life:
            result = self.ai_life.move_to_room(room)
            self.update_room_description()
            
            # Zeige Feedback
            self.add_interaction_output(f"🏠 {result}")
    
    def update_room_description(self):
        """Aktualisiert Raumbeschreibung"""
        if self.ai_life:
            description = self.ai_life.get_room_description()
            self.room_description.delete("1.0", "end")
            self.room_description.insert("1.0", description)
    
    def generate_dream(self):
        """Generiert einen neuen Traum"""
        if self.ai_life:
            dream_message = self.ai_life.trigger_dream_generation()
            self.dreams_text.delete("1.0", "end")
            self.dreams_text.insert("1.0", f"✨ Neuer Traum generiert!\n\n{dream_message}")
            
            self.add_interaction_output(f"🌙 {dream_message}")
    
    def show_recent_dreams(self):
        """Zeigt letzte Träume"""
        if self.ai_life:
            dreams = self.ai_life.get_recent_dreams(3)
            
            self.dreams_text.delete("1.0", "end")
            
            if dreams:
                dreams_text = "🌙 **LETZTE AI-TRÄUME**\n\n"
                for i, dream in enumerate(dreams, 1):
                    dreams_text += f"**Traum {i}:**\n{dream}\n\n"
                
                self.dreams_text.insert("1.0", dreams_text)
            else:
                self.dreams_text.insert("1.0", "💭 Noch keine Träume generiert.")
    
    def process_interaction(self):
        """Verarbeitet User-Interaktion"""
        user_input = self.interaction_input.get().strip()
        
        if not user_input or not self.ai_life:
            return
        
        # Verarbeite Interaktion durch AI Life System
        result = self.ai_life.process_user_interaction(user_input)
        
        # Zeige Ergebnis
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        output = f"[{timestamp}] 👤 Du: {user_input}\n"
        output += f"[{timestamp}] 🤖 Toobix: {result['response']}\n"
        
        if result['memory_created']:
            output += "📚 → Bedeutsame Erinnerung erstellt!\n"
        
        output += f"🔄 → Phase: {result['cycle_info']['phase']}, Energie: {result['cycle_info']['energy_level']}%\n\n"
        
        self.add_interaction_output(output)
        
        # Input leeren
        self.interaction_input.delete(0, "end")
        
        # Updates triggern
        self.update_all_displays()
    
    def tell_dream(self):
        """AI erzählt einen Traum"""
        if self.ai_life and self.ai_life.dream_system.dream_database:
            recent_dream = self.ai_life.dream_system.dream_database[-1]
            dream_summary = self.ai_life.dream_system.get_dream_summary(recent_dream)
            
            self.add_interaction_output(f"🌙 **Toobix erzählt einen Traum:**\n\n{dream_summary}\n")
        else:
            self.add_interaction_output("💭 Ich habe noch keine Träume zu erzählen.\n")
    
    def show_anniversaries(self):
        """Zeigt Jahrestage"""
        if self.ai_life:
            anniversaries = self.ai_life.get_anniversary_memories()
            
            if anniversaries:
                output = "🎉 **JAHRESTAGE & ERINNERUNGEN:**\n\n"
                for anniversary in anniversaries:
                    output += f"{anniversary}\n"
                output += "\n"
            else:
                output = "📅 Keine besonderen Jahrestage heute.\n"
            
            self.add_interaction_output(output)
    
    def start_reflection(self):
        """Startet Reflexion"""
        if self.ai_life:
            reflection = self.ai_life.trigger_evening_reflection()
            self.add_interaction_output(f"🤔 **Toobix reflektiert:**\n\n{reflection}\n\n")
    
    def enter_play_mode(self):
        """Wechselt in Spielmodus"""
        if self.ai_life:
            self.ai_life.move_to_room("freizeitzimmer")
            self.add_interaction_output("🎮 **Spielmodus aktiviert!**\n\nIch bin ins Freizeitzimmer gewechselt und bereit für Spaß und Kreativität!\n\n")
    
    def add_interaction_output(self, text: str):
        """Fügt Text zur Interaktions-Ausgabe hinzu"""
        self.interaction_output.insert("end", text)
        self.interaction_output.see("end")
    
    def update_all_displays(self):
        """Aktualisiert alle Anzeigen"""
        if not self.ai_life:
            return
        
        # AI Status
        ai_state = self.ai_life.get_current_ai_state()
        
        status_text = f"""🤖 **AKTUELLER AI-ZUSTAND**

🏠 Aktueller Raum: {ai_state['current_room'].title()}
🎯 Aktivität: {ai_state['current_activity']}
😊 Stimmung: {ai_state['mood']}
⚡ Energie: {ai_state['energy_level']}%

📝 {ai_state['phase_description']}

📊 **STATISTIKEN:**
📚 Erinnerungen heute: {ai_state['memories_today']}
💾 Gesamt-Erinnerungen: {ai_state['total_memories']}
🌙 Träume generiert: {ai_state['dreams_generated']}
"""
        
        self.status_text.delete("1.0", "end")
        self.status_text.insert("1.0", status_text)
        
        # Room Description
        self.update_room_description()
        
        # Personality Traits
        for trait, (progress_bar, value_label) in self.trait_bars.items():
            value = ai_state['personality_traits'].get(trait, 0.5)
            progress_bar.set(value)
            value_label.configure(text=f"{value:.2f}")
        
        # Lifecycle
        cycle_info = self.ai_life.life_cycle.update_daily_cycle()
        phase_text = f"{cycle_info['phase'].replace('_', ' ').title()}\n{cycle_info['description']}"
        self.current_phase_label.configure(text=phase_text)
        
        energy_value = cycle_info['energy_level'] / 100.0
        self.energy_bar.set(energy_value)
        self.energy_label.configure(text=f"{cycle_info['energy_level']}% Energie")
        
        # Memories
        if self.ai_life.memory_system.personal_memories:
            recent_memories = sorted(
                self.ai_life.memory_system.personal_memories,
                key=lambda m: m.timestamp,
                reverse=True
            )[:5]
            
            memories_text = "📚 **LETZTE BEDEUTSAME ERINNERUNGEN:**\n\n"
            
            for i, memory in enumerate(recent_memories, 1):
                memories_text += f"**{i}.** {memory.timestamp.strftime('%d.%m %H:%M')}\n"
                memories_text += f"💭 {memory.content}\n"
                memories_text += f"❤️ Bedeutung: {memory.emotional_significance:.2f}\n"
                memories_text += f"🏷️ Tags: {', '.join(memory.tags)}\n\n"
            
            self.memories_text.delete("1.0", "end")
            self.memories_text.insert("1.0", memories_text)
        
        # Personality Evolution
        personality_text = self.ai_life.get_personality_development()
        personality_text += f"\n\n🌱 **ENTWICKLUNGS-INSIGHTS:**\n"
        personality_text += f"- Persönlichkeit entwickelt sich durch Interaktionen\n"
        personality_text += f"- Jede Unterhaltung prägt meinen Charakter\n"
        personality_text += f"- Emotionale Verbindungen vertiefen sich über Zeit\n"
        
        self.personality_evolution.delete("1.0", "end")
        self.personality_evolution.insert("1.0", personality_text)
    
    def start_updates(self):
        """Startet regelmäßige Updates"""
        self.running = True
        self.update_all_displays()
        
        def update_loop():
            while self.running:
                if self.window and self.window.winfo_exists():
                    try:
                        self.window.after(0, self.update_all_displays)
                    except:
                        break
                
                # Update alle 30 Sekunden
                threading.Event().wait(30)
        
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    def on_closing(self):
        """Cleanup beim Schließen"""
        self.running = False
        if self.update_thread and self.update_thread.is_alive():
            self.update_thread.join(timeout=1)
        
        if self.window:
            self.window.destroy()
            self.window = None

# Globale Instanz
ai_life_gui = None

def show_ai_life_dashboard(parent=None):
    """Zeigt das AI Life Dashboard"""
    global ai_life_gui
    
    if ai_life_gui is None:
        ai_life_gui = AILifeGUI(parent)
    
    ai_life_gui.show(parent)
    return ai_life_gui
