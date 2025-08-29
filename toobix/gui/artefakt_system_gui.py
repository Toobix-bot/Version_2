"""
🎨 ARTEFAKT SYSTEM GUI
=====================

Visuelles Interface für Wisdom Crystallization:
- Artefakt Creation Studio
- Sacred Geometry Gallery
- Wisdom Collections Manager
- Healing Visualization Creator
- Image Generation Interface
- Energy Signature Viewer
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from typing import Dict, List, Any, Optional
import datetime
from pathlib import Path

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

from .artefakt_system import ArtefaktSystem, get_artefakt_system, initialize_artefakt_system

class ArtefaktSystemGUI:
    """
    🎨 ARTEFAKT CREATION STUDIO
    
    Visual Interface für:
    - Wisdom Artefakt Creation
    - Sacred Geometry Generation
    - Healing Visualization Design
    - Collection Management
    - Energy Analysis
    """
    
    def __init__(self, parent=None, ai_handler=None):
        self.parent = parent
        self.ai_handler = ai_handler
        self.window = None
        self.artefakt_system = None
        
    def show(self, parent=None):
        """Zeigt das Artefakt System Interface"""
        if parent:
            self.parent = parent
            
        if self.window is None or not self.window.winfo_exists():
            self.create_window()
        else:
            self.window.lift()
            self.window.focus()
    
    def create_window(self):
        """Erstellt das Artefakt System Fenster"""
        self.window = ctk.CTkToplevel(self.parent) if CTK_AVAILABLE else tk.Toplevel(self.parent)
        self.window.title("🎨 Artefakt System - Wisdom Crystallization Studio")
        self.window.geometry("1400x900")
        
        # Initialisiere Artefakt System
        self.artefakt_system = get_artefakt_system()
        if not self.artefakt_system:
            self.artefakt_system = initialize_artefakt_system(self.ai_handler)
        
        self.setup_gui()
        
        # Cleanup beim Schließen
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        """Erstellt die GUI-Elemente"""
        
        # Header mit magischem Design
        self.create_header()
        
        # Main Container mit Notebook
        main_container = ctk.CTkFrame(self.window) if CTK_AVAILABLE else ttk.Frame(self.window)
        main_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Notebook für verschiedene Studios
        if CTK_AVAILABLE:
            self.notebook = ctk.CTkTabview(main_container)
        else:
            self.notebook = ttk.Notebook(main_container)
        
        self.notebook.pack(fill="both", expand=True)
        
        # Tabs erstellen
        self.create_creation_studio_tab()
        self.create_sacred_geometry_tab()
        self.create_healing_studio_tab()
        self.create_collections_tab()
        self.create_gallery_tab()
        self.create_energy_analysis_tab()
    
    def create_header(self):
        """Erstellt magischen Header"""
        header = ctk.CTkFrame(self.window) if CTK_AVAILABLE else ttk.Frame(self.window)
        header.pack(fill="x", padx=10, pady=5)
        
        # Titel mit mystischen Symbolen
        title = ctk.CTkLabel(
            header,
            text="🎨 ✨ ARTEFAKT SYSTEM ✨ 🔮",
            font=ctk.CTkFont(size=24, weight="bold") if CTK_AVAILABLE else ("Arial", 20, "bold")
        ) if CTK_AVAILABLE else ttk.Label(header, text="🎨 ✨ ARTEFAKT SYSTEM ✨ 🔮", font=("Arial", 20, "bold"))
        title.pack(pady=10)
        
        # Mystischer Untertitel
        subtitle = ctk.CTkLabel(
            header,
            text="💫 Kristallisiere Weisheit in ewige Artefakte 💫",
            font=ctk.CTkFont(size=14, style="italic") if CTK_AVAILABLE else ("Arial", 12, "italic"),
            text_color="#9370DB" if CTK_AVAILABLE else None
        ) if CTK_AVAILABLE else ttk.Label(header, text="💫 Kristallisiere Weisheit in ewige Artefakte 💫", font=("Arial", 12, "italic"))
        subtitle.pack(pady=(0, 5))
        
        # Stats Display
        self.stats_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=10) if CTK_AVAILABLE else ("Arial", 9)
        ) if CTK_AVAILABLE else ttk.Label(header, text="", font=("Arial", 9))
        self.stats_label.pack(pady=2)
        
        self.update_stats_display()
    
    def create_creation_studio_tab(self):
        """Tab für Artefakt-Erstellung"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("✨ Creation Studio")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="✨ Creation Studio")
        
        # Left Panel - Wisdom Input
        left_panel = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Wisdom Input")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5), pady=5)
        
        # Wisdom Text Input
        wisdom_label = ctk.CTkLabel(left_panel, text="💎 Deine Weisheit / Erkenntnis:") if CTK_AVAILABLE else ttk.Label(left_panel, text="💎 Deine Weisheit / Erkenntnis:")
        wisdom_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.wisdom_text = ctk.CTkTextbox(
            left_panel,
            height=150,
            font=ctk.CTkFont(size=12),
            placeholder_text="Teile eine spirituelle Erkenntnis, ein inspirierendes Zitat oder eine transformative Wahrheit..."
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(left_panel, height=8, font=("Arial", 11))
        self.wisdom_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Artefakt Configuration
        config_frame = ctk.CTkFrame(left_panel) if CTK_AVAILABLE else ttk.LabelFrame(left_panel, text="Artefakt Konfiguration")
        config_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Category Selection
        category_frame = ctk.CTkFrame(config_frame) if CTK_AVAILABLE else ttk.Frame(config_frame)
        category_frame.pack(fill="x", padx=10, pady=5)
        
        category_label = ctk.CTkLabel(category_frame, text="Kategorie:") if CTK_AVAILABLE else ttk.Label(category_frame, text="Kategorie:")
        category_label.pack(side="left", padx=5)
        
        self.category_var = tk.StringVar(value="quote")
        categories = ["quote", "mandala", "visualization", "sacred_geometry", "healing"]
        category_menu = ctk.CTkOptionMenu(
            category_frame,
            values=categories,
            variable=self.category_var
        ) if CTK_AVAILABLE else ttk.Combobox(category_frame, textvariable=self.category_var, values=categories)
        category_menu.pack(side="left", padx=5)
        
        # Spiritual Theme
        theme_frame = ctk.CTkFrame(config_frame) if CTK_AVAILABLE else ttk.Frame(config_frame)
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        theme_label = ctk.CTkLabel(theme_frame, text="Spirituelles Thema:") if CTK_AVAILABLE else ttk.Label(theme_frame, text="Spirituelles Thema:")
        theme_label.pack(side="left", padx=5)
        
        self.theme_var = tk.StringVar(value="general")
        themes = ["general", "peace", "love", "wisdom", "healing", "manifestation", "protection"]
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=themes,
            variable=self.theme_var
        ) if CTK_AVAILABLE else ttk.Combobox(theme_frame, textvariable=self.theme_var, values=themes)
        theme_menu.pack(side="left", padx=5)
        
        # Title Input
        title_frame = ctk.CTkFrame(config_frame) if CTK_AVAILABLE else ttk.Frame(config_frame)
        title_frame.pack(fill="x", padx=10, pady=5)
        
        title_label = ctk.CTkLabel(title_frame, text="Titel (optional):") if CTK_AVAILABLE else ttk.Label(title_frame, text="Titel (optional):")
        title_label.pack(side="left", padx=5)
        
        self.title_entry = ctk.CTkEntry(
            title_frame,
            placeholder_text="Leer lassen für Auto-Generierung"
        ) if CTK_AVAILABLE else ttk.Entry(title_frame)
        self.title_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Custom Image Prompt
        prompt_label = ctk.CTkLabel(config_frame, text="🎨 Custom Image Prompt (optional):") if CTK_AVAILABLE else ttk.Label(config_frame, text="🎨 Custom Image Prompt (optional):")
        prompt_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.image_prompt_text = ctk.CTkTextbox(
            config_frame,
            height=80,
            placeholder_text="Spezifische Beschreibung für die Bildgenerierung..."
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(config_frame, height=4)
        self.image_prompt_text.pack(fill="x", padx=10, pady=5)
        
        # Create Button
        create_btn = ctk.CTkButton(
            left_panel,
            text="✨ Artefakt Erschaffen ✨",
            command=self.create_artefakt,
            font=ctk.CTkFont(size=16, weight="bold") if CTK_AVAILABLE else ("Arial", 14, "bold"),
            height=40
        ) if CTK_AVAILABLE else ttk.Button(left_panel, text="✨ Artefakt Erschaffen ✨", command=self.create_artefakt)
        create_btn.pack(pady=10)
        
        # Right Panel - Preview & Result
        right_panel = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Artefakt Preview")
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0), pady=5)
        
        # Current Artefakt Display
        self.artefakt_display = ctk.CTkTextbox(
            right_panel,
            font=ctk.CTkFont(size=11)
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(right_panel, font=("Arial", 10))
        self.artefakt_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Action Buttons
        action_frame = ctk.CTkFrame(right_panel) if CTK_AVAILABLE else ttk.Frame(right_panel)
        action_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        save_btn = ctk.CTkButton(
            action_frame,
            text="💾 Speichern",
            command=self.save_current_artefakt
        ) if CTK_AVAILABLE else ttk.Button(action_frame, text="💾 Speichern", command=self.save_current_artefakt)
        save_btn.pack(side="left", padx=5)
        
        collection_btn = ctk.CTkButton(
            action_frame,
            text="📚 Zu Collection",
            command=self.add_to_collection
        ) if CTK_AVAILABLE else ttk.Button(action_frame, text="📚 Zu Collection", command=self.add_to_collection)
        collection_btn.pack(side="left", padx=5)
        
        self.current_artefakt = None
    
    def create_sacred_geometry_tab(self):
        """Tab für Sacred Geometry"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("🔮 Sacred Geometry")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="🔮 Sacred Geometry")
        
        # Pattern Selection
        pattern_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Sacred Patterns")
        pattern_frame.pack(fill="x", padx=10, pady=5)
        
        patterns_info = {
            "flower_of_life": "🌸 Flower of Life - Schöpfungs-Geometrie",
            "merkaba": "⭐ Merkaba - Lichtkörper-Aktivierung",
            "sri_yantra": "🔺 Sri Yantra - Manifestations-Mandala",
            "tree_of_life": "🌳 Tree of Life - Kabbalistische Weisheit",
            "chakra_mandala": "🌈 Chakra Mandala - Energie-Zentren"
        }
        
        self.selected_pattern = tk.StringVar(value="flower_of_life")
        
        for pattern_id, description in patterns_info.items():
            pattern_radio = ctk.CTkRadioButton(
                pattern_frame,
                text=description,
                variable=self.selected_pattern,
                value=pattern_id
            ) if CTK_AVAILABLE else ttk.Radiobutton(pattern_frame, text=description, variable=self.selected_pattern, value=pattern_id)
            pattern_radio.pack(anchor="w", padx=10, pady=2)
        
        # Intention Input
        intention_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Intention")
        intention_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        intention_label = ctk.CTkLabel(intention_frame, text="✨ Deine Intention für dieses Sacred Pattern:") if CTK_AVAILABLE else ttk.Label(intention_frame, text="✨ Deine Intention für dieses Sacred Pattern:")
        intention_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.intention_text = ctk.CTkTextbox(
            intention_frame,
            height=100,
            placeholder_text="z.B. Ich aktiviere meine Lichtkörper-Energie für spirituelle Transformation..."
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(intention_frame, height=6)
        self.intention_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Generate Button
        generate_geometry_btn = ctk.CTkButton(
            intention_frame,
            text="🔮 Sacred Geometry Erschaffen",
            command=self.create_sacred_geometry,
            font=ctk.CTkFont(size=14, weight="bold") if CTK_AVAILABLE else ("Arial", 12, "bold")
        ) if CTK_AVAILABLE else ttk.Button(intention_frame, text="🔮 Sacred Geometry Erschaffen", command=self.create_sacred_geometry)
        generate_geometry_btn.pack(pady=10)
    
    def create_healing_studio_tab(self):
        """Tab für Healing Visualizations"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("💚 Healing Studio")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="💚 Healing Studio")
        
        # Healing Target
        target_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Healing Target")
        target_frame.pack(fill="x", padx=10, pady=5)
        
        target_label = ctk.CTkLabel(target_frame, text="🎯 Healing Bereich:") if CTK_AVAILABLE else ttk.Label(target_frame, text="🎯 Healing Bereich:")
        target_label.pack(side="left", padx=10)
        
        self.healing_target_var = tk.StringVar(value="general")
        healing_targets = ["general", "emotional", "physical", "mental", "spiritual"]
        target_menu = ctk.CTkOptionMenu(
            target_frame,
            values=healing_targets,
            variable=self.healing_target_var
        ) if CTK_AVAILABLE else ttk.Combobox(target_frame, textvariable=self.healing_target_var, values=healing_targets)
        target_menu.pack(side="left", padx=10)
        
        # Healing Intention
        healing_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Healing Intention")
        healing_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        healing_label = ctk.CTkLabel(healing_frame, text="💖 Deine Heilungs-Intention:") if CTK_AVAILABLE else ttk.Label(healing_frame, text="💖 Deine Heilungs-Intention:")
        healing_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.healing_intention_text = ctk.CTkTextbox(
            healing_frame,
            height=120,
            placeholder_text="z.B. Ich sende heilende Energie zu meinem Herzen für emotionale Balance und inneren Frieden..."
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(healing_frame, height=8)
        self.healing_intention_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Generate Healing Button
        generate_healing_btn = ctk.CTkButton(
            healing_frame,
            text="💚 Healing Artefakt Erschaffen",
            command=self.create_healing_artefakt,
            font=ctk.CTkFont(size=14, weight="bold") if CTK_AVAILABLE else ("Arial", 12, "bold")
        ) if CTK_AVAILABLE else ttk.Button(healing_frame, text="💚 Healing Artefakt Erschaffen", command=self.create_healing_artefakt)
        generate_healing_btn.pack(pady=10)
    
    def create_collections_tab(self):
        """Tab für Collection Management"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("📚 Collections")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="📚 Collections")
        
        # Collection Creator
        creator_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="New Collection")
        creator_frame.pack(fill="x", padx=10, pady=5)
        
        # Collection Name
        name_frame = ctk.CTkFrame(creator_frame) if CTK_AVAILABLE else ttk.Frame(creator_frame)
        name_frame.pack(fill="x", padx=10, pady=5)
        
        name_label = ctk.CTkLabel(name_frame, text="Collection Name:") if CTK_AVAILABLE else ttk.Label(name_frame, text="Collection Name:")
        name_label.pack(side="left", padx=5)
        
        self.collection_name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="z.B. Heilungs-Bibliothek"
        ) if CTK_AVAILABLE else ttk.Entry(name_frame)
        self.collection_name_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        # Collection Theme
        theme_frame = ctk.CTkFrame(creator_frame) if CTK_AVAILABLE else ttk.Frame(creator_frame)
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        coll_theme_label = ctk.CTkLabel(theme_frame, text="Theme:") if CTK_AVAILABLE else ttk.Label(theme_frame, text="Theme:")
        coll_theme_label.pack(side="left", padx=5)
        
        self.collection_theme_var = tk.StringVar(value="healing")
        collection_themes = ["healing", "manifestation", "peace", "love", "wisdom", "protection"]
        coll_theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=collection_themes,
            variable=self.collection_theme_var
        ) if CTK_AVAILABLE else ttk.Combobox(theme_frame, textvariable=self.collection_theme_var, values=collection_themes)
        coll_theme_menu.pack(side="left", padx=5)
        
        # Description
        desc_label = ctk.CTkLabel(creator_frame, text="Beschreibung:") if CTK_AVAILABLE else ttk.Label(creator_frame, text="Beschreibung:")
        desc_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.collection_desc_text = ctk.CTkTextbox(
            creator_frame,
            height=80
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(creator_frame, height=4)
        self.collection_desc_text.pack(fill="x", padx=10, pady=5)
        
        # Create Collection Button
        create_coll_btn = ctk.CTkButton(
            creator_frame,
            text="📚 Collection Erstellen",
            command=self.create_collection
        ) if CTK_AVAILABLE else ttk.Button(creator_frame, text="📚 Collection Erstellen", command=self.create_collection)
        create_coll_btn.pack(pady=10)
        
        # Collections List
        list_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="Existing Collections")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.collections_display = ctk.CTkTextbox(
            list_frame,
            font=ctk.CTkFont(size=11)
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(list_frame, font=("Arial", 10))
        self.collections_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Collection Actions
        coll_action_frame = ctk.CTkFrame(list_frame) if CTK_AVAILABLE else ttk.Frame(list_frame)
        coll_action_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        refresh_coll_btn = ctk.CTkButton(
            coll_action_frame,
            text="🔄 Refresh",
            command=self.refresh_collections_display
        ) if CTK_AVAILABLE else ttk.Button(coll_action_frame, text="🔄 Refresh", command=self.refresh_collections_display)
        refresh_coll_btn.pack(side="left", padx=5)
        
        export_coll_btn = ctk.CTkButton(
            coll_action_frame,
            text="📤 Export",
            command=self.export_collection
        ) if CTK_AVAILABLE else ttk.Button(coll_action_frame, text="📤 Export", command=self.export_collection)
        export_coll_btn.pack(side="left", padx=5)
        
        self.refresh_collections_display()
    
    def create_gallery_tab(self):
        """Tab für Artefakt Gallery"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("🖼️ Gallery")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="🖼️ Gallery")
        
        # Filter Options
        filter_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.Frame(tab_frame)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        filter_label = ctk.CTkLabel(filter_frame, text="Filter:") if CTK_AVAILABLE else ttk.Label(filter_frame, text="Filter:")
        filter_label.pack(side="left", padx=5)
        
        self.gallery_filter_var = tk.StringVar(value="all")
        filter_options = ["all", "quote", "mandala", "visualization", "sacred_geometry", "healing"]
        filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=filter_options,
            variable=self.gallery_filter_var,
            command=self.refresh_gallery_display
        ) if CTK_AVAILABLE else ttk.Combobox(filter_frame, textvariable=self.gallery_filter_var, values=filter_options)
        filter_menu.pack(side="left", padx=5)
        
        # Sort Options
        sort_label = ctk.CTkLabel(filter_frame, text="Sort by:") if CTK_AVAILABLE else ttk.Label(filter_frame, text="Sort by:")
        sort_label.pack(side="left", padx=(20, 5))
        
        self.gallery_sort_var = tk.StringVar(value="created_at")
        sort_options = ["created_at", "spiritual_energy", "manifestation_power", "healing_frequency"]
        sort_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=sort_options,
            variable=self.gallery_sort_var,
            command=self.refresh_gallery_display
        ) if CTK_AVAILABLE else ttk.Combobox(filter_frame, textvariable=self.gallery_sort_var, values=sort_options)
        sort_menu.pack(side="left", padx=5)
        
        # Gallery Display
        self.gallery_display = ctk.CTkTextbox(
            tab_frame,
            font=ctk.CTkFont(size=10)
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(tab_frame, font=("Arial", 9))
        self.gallery_display.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.refresh_gallery_display()
    
    def create_energy_analysis_tab(self):
        """Tab für Energy Analysis"""
        if CTK_AVAILABLE:
            tab_frame = self.notebook.add("⚡ Energy Analysis")
        else:
            tab_frame = ttk.Frame(self.notebook)
            self.notebook.add(tab_frame, text="⚡ Energy Analysis")
        
        # System Statistics
        stats_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="System Statistics")
        stats_frame.pack(fill="x", padx=10, pady=5)
        
        self.energy_stats_display = ctk.CTkTextbox(
            stats_frame,
            height=200,
            font=ctk.CTkFont(size=11)
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(stats_frame, height=10, font=("Arial", 10))
        self.energy_stats_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        # High Energy Artefakts
        high_energy_frame = ctk.CTkFrame(tab_frame) if CTK_AVAILABLE else ttk.LabelFrame(tab_frame, text="High Energy Artefakts")
        high_energy_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Energy Type Selection
        energy_type_frame = ctk.CTkFrame(high_energy_frame) if CTK_AVAILABLE else ttk.Frame(high_energy_frame)
        energy_type_frame.pack(fill="x", padx=10, pady=5)
        
        energy_label = ctk.CTkLabel(energy_type_frame, text="Energy Type:") if CTK_AVAILABLE else ttk.Label(energy_type_frame, text="Energy Type:")
        energy_label.pack(side="left", padx=5)
        
        self.energy_type_var = tk.StringVar(value="spiritual")
        energy_types = ["spiritual", "manifestation", "healing"]
        energy_menu = ctk.CTkOptionMenu(
            energy_type_frame,
            values=energy_types,
            variable=self.energy_type_var,
            command=self.refresh_energy_analysis
        ) if CTK_AVAILABLE else ttk.Combobox(energy_type_frame, textvariable=self.energy_type_var, values=energy_types)
        energy_menu.pack(side="left", padx=5)
        
        # Threshold Slider
        threshold_label = ctk.CTkLabel(energy_type_frame, text="Min Threshold:") if CTK_AVAILABLE else ttk.Label(energy_type_frame, text="Min Threshold:")
        threshold_label.pack(side="left", padx=(20, 5))
        
        self.energy_threshold_var = tk.DoubleVar(value=0.7)
        if CTK_AVAILABLE:
            threshold_slider = ctk.CTkSlider(
                energy_type_frame,
                from_=0.0,
                to=1.0,
                variable=self.energy_threshold_var,
                command=self.refresh_energy_analysis
            )
        else:
            threshold_slider = ttk.Scale(
                energy_type_frame,
                from_=0.0,
                to=1.0,
                variable=self.energy_threshold_var,
                command=self.refresh_energy_analysis
            )
        threshold_slider.pack(side="left", padx=5)
        
        self.threshold_value_label = ctk.CTkLabel(energy_type_frame, text="0.7") if CTK_AVAILABLE else ttk.Label(energy_type_frame, text="0.7")
        self.threshold_value_label.pack(side="left", padx=5)
        
        # High Energy Display
        self.high_energy_display = ctk.CTkTextbox(
            high_energy_frame,
            font=ctk.CTkFont(size=10)
        ) if CTK_AVAILABLE else scrolledtext.ScrolledText(high_energy_frame, font=("Arial", 9))
        self.high_energy_display.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.refresh_energy_analysis()
    
    def create_artefakt(self):
        """Erstellt ein neues Artefakt"""
        wisdom_text = self.wisdom_text.get("1.0", "end-1c") if CTK_AVAILABLE else self.wisdom_text.get("1.0", tk.END).strip()
        
        if not wisdom_text.strip():
            messagebox.showwarning("Warnung", "Bitte gib eine Weisheit ein!")
            return
        
        try:
            category = self.category_var.get()
            theme = self.theme_var.get()
            title = self.title_entry.get().strip() or None
            custom_prompt = self.image_prompt_text.get("1.0", "end-1c").strip() if CTK_AVAILABLE else self.image_prompt_text.get("1.0", tk.END).strip()
            custom_prompt = custom_prompt if custom_prompt else None
            
            # Erstelle Artefakt
            artefakt = self.artefakt_system.create_wisdom_artefakt(
                wisdom_text=wisdom_text,
                category=category,
                title=title,
                custom_prompt=custom_prompt,
                spiritual_theme=theme
            )
            
            self.current_artefakt = artefakt
            self.display_artefakt(artefakt)
            
            # Clear inputs
            self.wisdom_text.delete("1.0", "end") if CTK_AVAILABLE else self.wisdom_text.delete("1.0", tk.END)
            self.title_entry.delete(0, "end") if CTK_AVAILABLE else self.title_entry.delete(0, tk.END)
            self.image_prompt_text.delete("1.0", "end") if CTK_AVAILABLE else self.image_prompt_text.delete("1.0", tk.END)
            
            self.update_stats_display()
            messagebox.showinfo("Erfolg", f"✨ Artefakt '{artefakt.title}' erfolgreich erschaffen! ✨")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen des Artefakts: {e}")
    
    def create_sacred_geometry(self):
        """Erstellt Sacred Geometry Artefakt"""
        pattern_name = self.selected_pattern.get()
        intention = self.intention_text.get("1.0", "end-1c").strip() if CTK_AVAILABLE else self.intention_text.get("1.0", tk.END).strip()
        
        try:
            artefakt = self.artefakt_system.create_sacred_geometry_artefakt(pattern_name, intention)
            self.current_artefakt = artefakt
            self.display_artefakt(artefakt)
            
            # Clear intention
            self.intention_text.delete("1.0", "end") if CTK_AVAILABLE else self.intention_text.delete("1.0", tk.END)
            
            self.update_stats_display()
            messagebox.showinfo("Erfolg", f"🔮 Sacred Geometry '{artefakt.title}' manifestiert! 🔮")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen der Sacred Geometry: {e}")
    
    def create_healing_artefakt(self):
        """Erstellt Healing Artefakt"""
        intention = self.healing_intention_text.get("1.0", "end-1c").strip() if CTK_AVAILABLE else self.healing_intention_text.get("1.0", tk.END).strip()
        target_area = self.healing_target_var.get()
        
        if not intention:
            messagebox.showwarning("Warnung", "Bitte gib eine Heilungs-Intention ein!")
            return
        
        try:
            artefakt = self.artefakt_system.create_healing_artefakt(intention, target_area)
            self.current_artefakt = artefakt
            self.display_artefakt(artefakt)
            
            # Clear intention
            self.healing_intention_text.delete("1.0", "end") if CTK_AVAILABLE else self.healing_intention_text.delete("1.0", tk.END)
            
            self.update_stats_display()
            messagebox.showinfo("Erfolg", f"💚 Healing Artefakt '{artefakt.title}' aktiviert! 💚")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen des Healing Artefakts: {e}")
    
    def display_artefakt(self, artefakt):
        """Zeigt ein Artefakt im Display an"""
        display_text = f"✨ ARTEFAKT MANIFESTIERT ✨\n\n"
        display_text += f"🎨 TITEL: {artefakt.title}\n"
        display_text += f"📂 KATEGORIE: {artefakt.category.upper()}\n"
        display_text += f"🎯 THEMA: {artefakt.metadata.get('spiritual_theme', 'N/A')}\n"
        display_text += f"🕐 ERSTELLT: {artefakt.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        display_text += f"💎 WEISHEITS-TEXT:\n{artefakt.wisdom_text}\n\n"
        
        display_text += f"🎨 IMAGE PROMPT:\n{artefakt.image_prompt}\n\n"
        
        display_text += f"⚡ ENERGIE-SIGNATUR:\n"
        display_text += f"  🌟 Spirituell: {artefakt.spiritual_energy:.3f}\n"
        display_text += f"  ✨ Manifestation: {artefakt.manifestation_power:.3f}\n"
        display_text += f"  💚 Heilung: {artefakt.healing_frequency:.3f}\n\n"
        
        display_text += f"🏷️ TAGS: {', '.join(artefakt.tags)}\n\n"
        
        if artefakt.image_path:
            display_text += f"🖼️ BILD: {artefakt.image_path}\n"
            display_text += f"📊 STATUS: {artefakt.metadata.get('image_status', 'unknown')}\n"
        else:
            display_text += f"🖼️ BILD: Wird generiert...\n"
        
        self.artefakt_display.delete("1.0", "end") if CTK_AVAILABLE else self.artefakt_display.delete("1.0", tk.END)
        self.artefakt_display.insert("1.0", display_text)
    
    def save_current_artefakt(self):
        """Speichert das aktuelle Artefakt"""
        if not self.current_artefakt:
            messagebox.showwarning("Warnung", "Kein Artefakt zum Speichern ausgewählt!")
            return
        
        try:
            # Artefakt ist bereits im System gespeichert
            messagebox.showinfo("Gespeichert", f"Artefakt '{self.current_artefakt.title}' wurde gespeichert!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")
    
    def add_to_collection(self):
        """Fügt aktuelles Artefakt zu einer Collection hinzu"""
        if not self.current_artefakt:
            messagebox.showwarning("Warnung", "Kein Artefakt ausgewählt!")
            return
        
        # Simple dialog für Collection-Auswahl
        collection_names = [coll.name for coll.id, coll in self.artefakt_system.collections.items()]
        
        if not collection_names:
            messagebox.showinfo("Info", "Keine Collections verfügbar. Erstelle zuerst eine Collection!")
            return
        
        # For simplicity, add to first collection
        # In a real implementation, you'd show a selection dialog
        first_collection_id = list(self.artefakt_system.collections.keys())[0]
        self.artefakt_system.add_to_collection(first_collection_id, self.current_artefakt.id)
        messagebox.showinfo("Erfolg", "Artefakt zur Collection hinzugefügt!")
    
    def create_collection(self):
        """Erstellt eine neue Collection"""
        name = self.collection_name_entry.get().strip()
        theme = self.collection_theme_var.get()
        description = self.collection_desc_text.get("1.0", "end-1c").strip() if CTK_AVAILABLE else self.collection_desc_text.get("1.0", tk.END).strip()
        
        if not name:
            messagebox.showwarning("Warnung", "Bitte gib einen Collection-Namen ein!")
            return
        
        try:
            collection = self.artefakt_system.create_collection(name, description, theme)
            
            # Clear inputs
            self.collection_name_entry.delete(0, "end") if CTK_AVAILABLE else self.collection_name_entry.delete(0, tk.END)
            self.collection_desc_text.delete("1.0", "end") if CTK_AVAILABLE else self.collection_desc_text.delete("1.0", tk.END)
            
            self.refresh_collections_display()
            messagebox.showinfo("Erfolg", f"📚 Collection '{collection.name}' erstellt!")
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen der Collection: {e}")
    
    def refresh_collections_display(self):
        """Aktualisiert die Collections-Anzeige"""
        display_text = "📚 WISDOM COLLECTIONS\n\n"
        
        if not self.artefakt_system.collections:
            display_text += "Noch keine Collections erstellt.\n"
        else:
            for collection in self.artefakt_system.collections.values():
                display_text += f"📚 {collection.name}\n"
                display_text += f"   🎯 Theme: {collection.theme}\n"
                display_text += f"   📝 {collection.description[:100]}...\n" if len(collection.description) > 100 else f"   📝 {collection.description}\n"
                display_text += f"   📊 Artefakte: {len(collection.artefakts)}\n"
                display_text += f"   🕐 Erstellt: {collection.created_at.strftime('%d.%m.%Y')}\n"
                
                if collection.energy_signature:
                    display_text += f"   ⚡ Energie: S:{collection.energy_signature.get('spiritual', 0):.2f} M:{collection.energy_signature.get('manifestation', 0):.2f} H:{collection.energy_signature.get('healing', 0):.2f}\n"
                
                display_text += "\n"
        
        self.collections_display.delete("1.0", "end") if CTK_AVAILABLE else self.collections_display.delete("1.0", tk.END)
        self.collections_display.insert("1.0", display_text)
    
    def export_collection(self):
        """Exportiert eine Collection"""
        if not self.artefakt_system.collections:
            messagebox.showinfo("Info", "Keine Collections zum Exportieren verfügbar!")
            return
        
        # For simplicity, export first collection
        first_collection_id = list(self.artefakt_system.collections.keys())[0]
        
        try:
            filepath = self.artefakt_system.export_collection(first_collection_id)
            messagebox.showinfo("Export Erfolg", f"Collection exportiert nach:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Export Fehler", f"Fehler beim Exportieren: {e}")
    
    def refresh_gallery_display(self, *args):
        """Aktualisiert die Gallery-Anzeige"""
        filter_category = self.gallery_filter_var.get()
        sort_by = self.gallery_sort_var.get()
        
        # Filter artefakts
        if filter_category == "all":
            artefakts = list(self.artefakt_system.artefakts.values())
        else:
            artefakts = [a for a in self.artefakt_system.artefakts.values() if a.category == filter_category]
        
        # Sort artefakts
        if sort_by == "created_at":
            artefakts.sort(key=lambda a: a.created_at, reverse=True)
        elif sort_by == "spiritual_energy":
            artefakts.sort(key=lambda a: a.spiritual_energy, reverse=True)
        elif sort_by == "manifestation_power":
            artefakts.sort(key=lambda a: a.manifestation_power, reverse=True)
        elif sort_by == "healing_frequency":
            artefakts.sort(key=lambda a: a.healing_frequency, reverse=True)
        
        # Display artefakts
        display_text = f"🖼️ ARTEFAKT GALLERY ({len(artefakts)} Artefakte)\n\n"
        
        for artefakt in artefakts[:20]:  # Show only first 20
            display_text += f"✨ {artefakt.title}\n"
            display_text += f"   📂 {artefakt.category} | 🎯 {artefakt.metadata.get('spiritual_theme', 'N/A')}\n"
            display_text += f"   💎 {artefakt.wisdom_text[:80]}...\n" if len(artefakt.wisdom_text) > 80 else f"   💎 {artefakt.wisdom_text}\n"
            display_text += f"   ⚡ S:{artefakt.spiritual_energy:.2f} M:{artefakt.manifestation_power:.2f} H:{artefakt.healing_frequency:.2f}\n"
            display_text += f"   🕐 {artefakt.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
        
        self.gallery_display.delete("1.0", "end") if CTK_AVAILABLE else self.gallery_display.delete("1.0", tk.END)
        self.gallery_display.insert("1.0", display_text)
    
    def refresh_energy_analysis(self, *args):
        """Aktualisiert die Energy Analysis"""
        # Update threshold label
        threshold = self.energy_threshold_var.get()
        self.threshold_value_label.configure(text=f"{threshold:.2f}")
        
        # Get high energy artefakts
        energy_type = self.energy_type_var.get()
        high_energy_artefakts = self.artefakt_system.get_high_energy_artefakts(energy_type, threshold)
        
        # System statistics
        stats = self.artefakt_system.get_statistics()
        
        stats_text = "⚡ ARTEFAKT SYSTEM ENERGIE-ANALYSE\n\n"
        stats_text += f"📊 SYSTEM STATISTIKEN:\n"
        stats_text += f"   🎨 Total Artefakte: {stats['total_artefakts']}\n"
        stats_text += f"   📚 Total Collections: {stats['total_collections']}\n"
        stats_text += f"   🖼️ Image Generation: {'✅ Verfügbar' if stats['image_generation_available'] else '❌ Nicht verfügbar'}\n\n"
        
        stats_text += f"📂 KATEGORIEN:\n"
        for category, count in stats['categories'].items():
            stats_text += f"   {category}: {count}\n"
        stats_text += "\n"
        
        stats_text += f"🎯 THEMEN:\n"
        for theme, count in stats['themes'].items():
            stats_text += f"   {theme}: {count}\n"
        stats_text += "\n"
        
        stats_text += f"⚡ DURCHSCHNITTLICHE ENERGIEN:\n"
        for energy, value in stats['average_energies'].items():
            stats_text += f"   {energy}: {value:.3f}\n"
        
        self.energy_stats_display.delete("1.0", "end") if CTK_AVAILABLE else self.energy_stats_display.delete("1.0", tk.END)
        self.energy_stats_display.insert("1.0", stats_text)
        
        # High energy artefakts
        high_energy_text = f"🔥 HIGH {energy_type.upper()} ENERGY ARTEFAKTE (≥{threshold:.2f})\n\n"
        
        if not high_energy_artefakts:
            high_energy_text += "Keine Artefakte über dem Threshold gefunden.\n"
        else:
            for artefakt in high_energy_artefakts[:10]:  # Top 10
                energy_value = getattr(artefakt, f"{energy_type}_energy" if energy_type == "spiritual" else f"{energy_type}_power" if energy_type == "manifestation" else f"{energy_type}_frequency")
                high_energy_text += f"⚡ {artefakt.title}\n"
                high_energy_text += f"   🔥 {energy_type.title()} Energy: {energy_value:.3f}\n"
                high_energy_text += f"   📂 {artefakt.category} | 🎯 {artefakt.metadata.get('spiritual_theme', 'N/A')}\n"
                high_energy_text += f"   💎 {artefakt.wisdom_text[:60]}...\n\n"
        
        self.high_energy_display.delete("1.0", "end") if CTK_AVAILABLE else self.high_energy_display.delete("1.0", tk.END)
        self.high_energy_display.insert("1.0", high_energy_text)
    
    def update_stats_display(self):
        """Aktualisiert die Statistik-Anzeige im Header"""
        stats = self.artefakt_system.get_statistics()
        stats_text = f"📊 {stats['total_artefakts']} Artefakte | 📚 {stats['total_collections']} Collections | ⚡ Ø Spiritual: {stats['average_energies'].get('spiritual', 0):.2f}"
        self.stats_label.configure(text=stats_text)
    
    def on_closing(self):
        """Cleanup beim Schließen"""
        if self.window:
            self.window.destroy()
            self.window = None

# Globale Instanz
artefakt_gui = None

def show_artefakt_system(parent=None, ai_handler=None):
    """Zeigt das Artefakt System Interface"""
    global artefakt_gui
    
    if artefakt_gui is None:
        artefakt_gui = ArtefaktSystemGUI(parent, ai_handler)
    
    artefakt_gui.show(parent)
    return artefakt_gui
