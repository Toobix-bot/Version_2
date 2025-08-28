"""
Toobix Phase 4 GUI Extensions
Erweiterte GUI-Panels für System-Transparenz und erweiterte Features
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import threading
import time
from pathlib import Path

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

class DocumentationPanel:
    """Panel für System-Dokumentation"""
    
    def __init__(self, parent, documentation_engine):
        self.parent = parent
        self.documentation_engine = documentation_engine
        self.panel = None
        self.content_area = None
        self.search_entry = None
        self.category_list = None
        
        self._create_panel()
    
    def _create_panel(self):
        """Erstellt Dokumentations-Panel"""
        if CTK_AVAILABLE:
            self.panel = ctk.CTkFrame(self.parent)
        else:
            self.panel = ttk.Frame(self.parent)
        
        # Header
        header_label = self._create_label("📚 System-Dokumentation", font=("Arial", 14, "bold"))
        header_label.pack(pady=10)
        
        # Such-Bereich
        search_frame = self._create_frame()
        search_frame.pack(fill="x", padx=10, pady=5)
        
        search_label = self._create_label("Suche:")
        search_label.pack(side="left")
        
        if CTK_AVAILABLE:
            self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Funktion oder Komponente suchen...")
        else:
            self.search_entry = ttk.Entry(search_frame)
        
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.search_entry.bind('<KeyRelease>', self._on_search)
        
        # Content-Bereich
        content_frame = self._create_frame()
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Kategorien-Liste
        categories_frame = self._create_frame(content_frame)
        categories_frame.pack(side="left", fill="y", padx=(0, 5))
        
        categories_label = self._create_label(categories_frame, "Kategorien:", font=("Arial", 10, "bold"))
        categories_label.pack()
        
        if CTK_AVAILABLE:
            self.category_list = tk.Listbox(categories_frame, height=15, width=20)
        else:
            self.category_list = tk.Listbox(categories_frame, height=15, width=20)
        
        self.category_list.pack(fill="y", expand=True)
        self.category_list.bind('<<ListboxSelect>>', self._on_category_select)
        
        # Content-Area
        if CTK_AVAILABLE:
            self.content_area = ctk.CTkTextbox(content_frame, height=300)
        else:
            self.content_area = scrolledtext.ScrolledText(content_frame, height=15, wrap=tk.WORD)
        
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Lade initiale Daten
        self._load_categories()
        self._load_overview()
    
    def _create_frame(self, parent=None):
        """Erstellt Frame"""
        parent = parent or self.panel
        if CTK_AVAILABLE:
            return ctk.CTkFrame(parent)
        else:
            return ttk.Frame(parent)
    
    def _create_label(self, parent_or_text, text=None, **kwargs):
        """Erstellt Label"""
        if text is None:
            text = parent_or_text
            parent = self.panel
        else:
            parent = parent_or_text
        
        if CTK_AVAILABLE:
            return ctk.CTkLabel(parent, text=text, **kwargs)
        else:
            return ttk.Label(parent, text=text, **kwargs)
    
    def _load_categories(self):
        """Lädt Kategorien"""
        try:
            categories = self.documentation_engine.get_component_categories()
            self.category_list.delete(0, tk.END)
            for category in categories:
                self.category_list.insert(tk.END, category)
        except Exception as e:
            print(f"Kategorie-Lade-Fehler: {e}")
    
    def _load_overview(self):
        """Lädt System-Übersicht"""
        try:
            overview = self.documentation_engine.get_system_overview()
            self._display_content("System-Übersicht", overview)
        except Exception as e:
            self._display_content("Fehler", f"Fehler beim Laden der Übersicht: {e}")
    
    def _on_category_select(self, event):
        """Kategorie-Auswahl Handler"""
        selection = self.category_list.curselection()
        if selection:
            category = self.category_list.get(selection[0])
            try:
                components = self.documentation_engine.get_components_by_category(category)
                content = f"Komponenten in {category}:\n\n"
                for comp in components:
                    content += f"• {comp['name']}: {comp['description']}\n"
                self._display_content(f"Kategorie: {category}", content)
            except Exception as e:
                self._display_content("Fehler", f"Fehler beim Laden der Kategorie: {e}")
    
    def _on_search(self, event):
        """Such-Handler"""
        query = self.search_entry.get()
        if len(query) >= 2:
            try:
                results = self.documentation_engine.search_functions(query)
                content = f"Suchergebnisse für '{query}':\n\n"
                for result in results[:10]:  # Top 10 Ergebnisse
                    content += f"• {result['name']}: {result['description']}\n"
                    content += f"  Kategorie: {result['category']}\n\n"
                self._display_content(f"Suche: {query}", content)
            except Exception as e:
                self._display_content("Fehler", f"Such-Fehler: {e}")
    
    def _display_content(self, title, content):
        """Zeigt Content an"""
        try:
            if CTK_AVAILABLE:
                self.content_area.delete("1.0", tk.END)
                self.content_area.insert("1.0", f"{title}\n{'='*len(title)}\n\n{content}")
            else:
                self.content_area.delete("1.0", tk.END)
                self.content_area.insert("1.0", f"{title}\n{'='*len(title)}\n\n{content}")
        except Exception as e:
            print(f"Content-Display Fehler: {e}")


class ThoughtStreamPanel:
    """Panel für KI-Gedankenstrom"""
    
    def __init__(self, parent, thought_stream_engine):
        self.parent = parent
        self.thought_stream_engine = thought_stream_engine
        self.panel = None
        self.thoughts_display = None
        self.filter_var = None
        self.auto_scroll = tk.BooleanVar(value=True)
        
        self._create_panel()
        self._start_update_loop()
    
    def _create_panel(self):
        """Erstellt Gedankenstrom-Panel"""
        if CTK_AVAILABLE:
            self.panel = ctk.CTkFrame(self.parent)
        else:
            self.panel = ttk.Frame(self.parent)
        
        # Header
        header_label = self._create_label("🧠 KI-Gedankenstrom", font=("Arial", 14, "bold"))
        header_label.pack(pady=10)
        
        # Kontroll-Bereich
        controls_frame = self._create_frame()
        controls_frame.pack(fill="x", padx=10, pady=5)
        
        # Filter
        filter_label = self._create_label(controls_frame, "Filter:")
        filter_label.pack(side="left")
        
        self.filter_var = tk.StringVar(value="all")
        if CTK_AVAILABLE:
            filter_menu = ctk.CTkOptionMenu(
                controls_frame,
                variable=self.filter_var,
                values=["all", "insights", "suggestions", "observations", "ideas", "warnings"]
            )
        else:
            filter_menu = ttk.Combobox(
                controls_frame,
                textvariable=self.filter_var,
                values=["all", "insights", "suggestions", "observations", "ideas", "warnings"],
                state="readonly"
            )
        
        filter_menu.pack(side="left", padx=5)
        
        # Auto-Scroll Checkbox
        if CTK_AVAILABLE:
            scroll_check = ctk.CTkCheckBox(controls_frame, text="Auto-Scroll", variable=self.auto_scroll)
        else:
            scroll_check = ttk.Checkbutton(controls_frame, text="Auto-Scroll", variable=self.auto_scroll)
        
        scroll_check.pack(side="right")
        
        # Gedanken-Display
        if CTK_AVAILABLE:
            self.thoughts_display = ctk.CTkTextbox(self.panel, height=400)
        else:
            self.thoughts_display = scrolledtext.ScrolledText(self.panel, height=20, wrap=tk.WORD)
        
        self.thoughts_display.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Initial-Nachricht
        self._add_thought_to_display("System", "KI-Gedankenstrom initialisiert. Gedanken werden hier angezeigt...", "info")
    
    def _create_frame(self, parent=None):
        """Erstellt Frame"""
        parent = parent or self.panel
        if CTK_AVAILABLE:
            return ctk.CTkFrame(parent)
        else:
            return ttk.Frame(parent)
    
    def _create_label(self, parent_or_text, text=None, **kwargs):
        """Erstellt Label"""
        if text is None:
            text = parent_or_text
            parent = self.panel
        else:
            parent = parent_or_text
        
        if CTK_AVAILABLE:
            return ctk.CTkLabel(parent, text=text, **kwargs)
        else:
            return ttk.Label(parent, text=text, **kwargs)
    
    def _start_update_loop(self):
        """Startet Update-Loop für Gedanken"""
        def update_thoughts():
            while True:
                try:
                    # Hole neue Gedanken
                    thoughts = self.thought_stream_engine.get_thought_stream(5)
                    
                    # Update GUI im Main Thread
                    self.parent.after(0, lambda: self._update_thoughts_display(thoughts))
                    
                    time.sleep(10)  # Update alle 10 Sekunden
                except Exception as e:
                    print(f"Thought Update Fehler: {e}")
                    time.sleep(30)
        
        update_thread = threading.Thread(target=update_thoughts, daemon=True)
        update_thread.start()
    
    def _update_thoughts_display(self, thoughts):
        """Update Gedanken-Display"""
        try:
            current_filter = self.filter_var.get()
            
            for thought in thoughts:
                thought_type = thought.get('thought_type', 'unknown')
                
                # Filter anwenden
                if current_filter != "all" and thought_type != current_filter:
                    continue
                
                # Gedanken hinzufügen
                content = thought.get('content', 'Kein Inhalt')
                timestamp = thought.get('timestamp', '')
                
                self._add_thought_to_display(thought_type, content, timestamp)
                
        except Exception as e:
            print(f"Thoughts Display Update Fehler: {e}")
    
    def _add_thought_to_display(self, thought_type, content, timestamp):
        """Fügt Gedanken zu Display hinzu"""
        try:
            # Icon basierend auf Typ
            icons = {
                'insight': '💡',
                'suggestion': '💭',
                'observation': '👁️',
                'idea': '🌟',
                'warning': '⚠️',
                'info': 'ℹ️',
                'system': '⚙️'
            }
            
            icon = icons.get(thought_type, '🤔')
            
            # Formatiere Nachricht
            if isinstance(timestamp, str):
                time_str = timestamp[:19] if len(timestamp) > 19 else timestamp
            else:
                time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            message = f"[{time_str}] {icon} {thought_type.upper()}: {content}\n\n"
            
            # Füge zu Display hinzu
            if CTK_AVAILABLE:
                self.thoughts_display.insert(tk.END, message)
            else:
                self.thoughts_display.insert(tk.END, message)
            
            # Auto-Scroll
            if self.auto_scroll.get():
                if CTK_AVAILABLE:
                    self.thoughts_display.see(tk.END)
                else:
                    self.thoughts_display.see(tk.END)
                    
        except Exception as e:
            print(f"Add Thought Fehler: {e}")


class ExtendedSettingsPanel:
    """Panel für erweiterte Einstellungen"""
    
    def __init__(self, parent, extended_settings):
        self.parent = parent
        self.extended_settings = extended_settings
        self.panel = None
        self.category_tree = None
        self.settings_frame = None
        self.current_category = None
        
        self._create_panel()
        self._load_categories()
    
    def _create_panel(self):
        """Erstellt Einstellungs-Panel"""
        if CTK_AVAILABLE:
            self.panel = ctk.CTkFrame(self.parent)
        else:
            self.panel = ttk.Frame(self.parent)
        
        # Header
        header_label = self._create_label("⚙️ Erweiterte Einstellungen", font=("Arial", 14, "bold"))
        header_label.pack(pady=10)
        
        # Main Content Frame
        main_frame = self._create_frame()
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Kategorien-Tree (links)
        tree_frame = self._create_frame(main_frame)
        tree_frame.pack(side="left", fill="y", padx=(0, 10))
        
        tree_label = self._create_label(tree_frame, "Kategorien:")
        tree_label.pack()
        
        self.category_tree = ttk.Treeview(tree_frame, height=15, width=25)
        self.category_tree.pack(fill="y", expand=True)
        self.category_tree.bind('<<TreeviewSelect>>', self._on_category_select)
        
        # Einstellungs-Bereich (rechts)
        self.settings_frame = self._create_frame(main_frame)
        self.settings_frame.pack(side="right", fill="both", expand=True)
        
        settings_label = self._create_label(self.settings_frame, "Einstellungen:")
        settings_label.pack()
    
    def _create_frame(self, parent=None):
        """Erstellt Frame"""
        parent = parent or self.panel
        if CTK_AVAILABLE:
            return ctk.CTkFrame(parent)
        else:
            return ttk.Frame(parent)
    
    def _create_label(self, parent_or_text, text=None, **kwargs):
        """Erstellt Label"""
        if text is None:
            text = parent_or_text
            parent = self.panel
        else:
            parent = parent_or_text
        
        if CTK_AVAILABLE:
            return ctk.CTkLabel(parent, text=text, **kwargs)
        else:
            return ttk.Label(parent, text=text, **kwargs)
    
    def _load_categories(self):
        """Lädt Kategorien in Tree"""
        try:
            categories = self.extended_settings.get_all_categories()
            
            for category in categories:
                self.category_tree.insert("", "end", text=category, values=[category])
                
        except Exception as e:
            print(f"Kategorie-Lade-Fehler: {e}")
    
    def _on_category_select(self, event):
        """Kategorie-Auswahl Handler"""
        selection = self.category_tree.selection()
        if selection:
            item = self.category_tree.item(selection[0])
            category = item['values'][0] if item['values'] else item['text']
            self._load_category_settings(category)
    
    def _load_category_settings(self, category):
        """Lädt Einstellungen für Kategorie"""
        try:
            # Lösche alte Einstellungen
            for widget in self.settings_frame.winfo_children():
                if widget.winfo_class() != 'Label':  # Behalte das Label
                    widget.destroy()
            
            # Hole Einstellungen für Kategorie
            settings = self.extended_settings.get_settings_by_category(category)
            
            # Scroll-Frame für viele Einstellungen
            if CTK_AVAILABLE:
                scroll_frame = ctk.CTkScrollableFrame(self.settings_frame)
            else:
                # Vereinfachte Version ohne Scroll für tkinter
                scroll_frame = ttk.Frame(self.settings_frame)
            
            scroll_frame.pack(fill="both", expand=True, pady=10)
            
            # Erstelle Einstellungs-Widgets
            for key, setting in settings.items():
                self._create_setting_widget(scroll_frame, key, setting)
            
            self.current_category = category
            
        except Exception as e:
            print(f"Settings Load Fehler: {e}")
    
    def _create_setting_widget(self, parent, key, setting):
        """Erstellt Widget für eine Einstellung"""
        try:
            # Haupt-Frame für diese Einstellung
            setting_frame = self._create_frame(parent)
            setting_frame.pack(fill="x", pady=5, padx=10)
            
            # Label mit Namen und Beschreibung
            label_text = f"{setting.display_name}"
            if setting.description:
                label_text += f"\n({setting.description})"
            
            label = self._create_label(setting_frame, label_text)
            label.pack(anchor="w")
            
            # Widget basierend auf Typ
            current_value = setting.current_value
            
            if setting.value_type == 'bool':
                var = tk.BooleanVar(value=current_value)
                if CTK_AVAILABLE:
                    widget = ctk.CTkCheckBox(setting_frame, text="", variable=var)
                else:
                    widget = ttk.Checkbutton(setting_frame, variable=var)
                
                widget.pack(anchor="w", pady=2)
                widget.configure(command=lambda: self._save_setting(key, var.get()))
                
            elif setting.value_type in ['int', 'float']:
                var = tk.StringVar(value=str(current_value))
                if CTK_AVAILABLE:
                    widget = ctk.CTkEntry(setting_frame, textvariable=var)
                else:
                    widget = ttk.Entry(setting_frame, textvariable=var)
                
                widget.pack(anchor="w", pady=2, fill="x")
                widget.bind('<KeyRelease>', lambda e: self._validate_numeric_setting(key, setting, var))
                
            elif setting.value_type == 'string':
                if setting.options:
                    # Dropdown für Optionen
                    var = tk.StringVar(value=current_value)
                    if CTK_AVAILABLE:
                        widget = ctk.CTkOptionMenu(setting_frame, variable=var, values=setting.options)
                    else:
                        widget = ttk.Combobox(setting_frame, textvariable=var, values=setting.options, state="readonly")
                    
                    widget.pack(anchor="w", pady=2)
                    var.trace('w', lambda *args: self._save_setting(key, var.get()))
                else:
                    # Text-Eingabe
                    var = tk.StringVar(value=current_value)
                    if CTK_AVAILABLE:
                        widget = ctk.CTkEntry(setting_frame, textvariable=var)
                    else:
                        widget = ttk.Entry(setting_frame, textvariable=var)
                    
                    widget.pack(anchor="w", pady=2, fill="x")
                    widget.bind('<KeyRelease>', lambda e: self._save_setting(key, var.get()))
            
            # Tooltip falls vorhanden
            if setting.tooltip and not CTK_AVAILABLE:
                # Einfacher Tooltip für tkinter
                def show_tooltip(event):
                    tooltip = tk.Toplevel()
                    tooltip.wm_overrideredirect(True)
                    tooltip.wm_geometry(f"+{event.x_root}+{event.y_root}")
                    label = tk.Label(tooltip, text=setting.tooltip, background="yellow")
                    label.pack()
                    tooltip.after(3000, tooltip.destroy)
                
                widget.bind('<Double-Button-1>', show_tooltip)
                    
        except Exception as e:
            print(f"Setting Widget Fehler: {e}")
    
    def _validate_numeric_setting(self, key, setting, var):
        """Validiert numerische Einstellung"""
        try:
            value_str = var.get()
            if setting.value_type == 'int':
                value = int(value_str)
            else:
                value = float(value_str)
            
            # Validiere Grenzen
            if setting.min_value is not None and value < setting.min_value:
                return
            if setting.max_value is not None and value > setting.max_value:
                return
            
            self._save_setting(key, value)
            
        except ValueError:
            # Ungültiger Wert, ignorieren
            pass
    
    def _save_setting(self, key, value):
        """Speichert Einstellung"""
        try:
            success = self.extended_settings.set_setting(key, value)
            if success:
                print(f"Einstellung gespeichert: {key} = {value}")
            else:
                print(f"Fehler beim Speichern von {key}")
        except Exception as e:
            print(f"Save Setting Fehler: {e}")


class TutorialPanel:
    """Panel für interaktive Tutorials"""
    
    def __init__(self, parent, tutorial_system):
        self.parent = parent
        self.tutorial_system = tutorial_system
        self.panel = None
        self.tutorial_list = None
        self.tutorial_info = None
        self.current_tutorial = None
        
        self._create_panel()
        self._load_tutorials()
    
    def _create_panel(self):
        """Erstellt Tutorial-Panel"""
        if CTK_AVAILABLE:
            self.panel = ctk.CTkFrame(self.parent)
        else:
            self.panel = ttk.Frame(self.parent)
        
        # Header
        header_label = self._create_label("🎓 Interaktive Tutorials", font=("Arial", 14, "bold"))
        header_label.pack(pady=10)
        
        # Main Content
        main_frame = self._create_frame()
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tutorial-Liste (links)
        list_frame = self._create_frame(main_frame)
        list_frame.pack(side="left", fill="y", padx=(0, 10))
        
        list_label = self._create_label(list_frame, "Verfügbare Tutorials:")
        list_label.pack()
        
        self.tutorial_list = tk.Listbox(list_frame, height=15, width=30)
        self.tutorial_list.pack(fill="y", expand=True)
        self.tutorial_list.bind('<<ListboxSelect>>', self._on_tutorial_select)
        
        # Tutorial-Info (rechts)
        info_frame = self._create_frame(main_frame)
        info_frame.pack(side="right", fill="both", expand=True)
        
        info_label = self._create_label(info_frame, "Tutorial-Informationen:")
        info_label.pack()
        
        if CTK_AVAILABLE:
            self.tutorial_info = ctk.CTkTextbox(info_frame, height=300)
        else:
            self.tutorial_info = scrolledtext.ScrolledText(info_frame, height=15, wrap=tk.WORD)
        
        self.tutorial_info.pack(fill="both", expand=True, pady=10)
        
        # Buttons
        button_frame = self._create_frame(info_frame)
        button_frame.pack(fill="x", pady=10)
        
        if CTK_AVAILABLE:
            start_btn = ctk.CTkButton(button_frame, text="Tutorial starten", command=self._start_tutorial)
            stop_btn = ctk.CTkButton(button_frame, text="Tutorial stoppen", command=self._stop_tutorial)
        else:
            start_btn = ttk.Button(button_frame, text="Tutorial starten", command=self._start_tutorial)
            stop_btn = ttk.Button(button_frame, text="Tutorial stoppen", command=self._stop_tutorial)
        
        start_btn.pack(side="left", padx=5)
        stop_btn.pack(side="left", padx=5)
    
    def _create_frame(self, parent=None):
        """Erstellt Frame"""
        parent = parent or self.panel
        if CTK_AVAILABLE:
            return ctk.CTkFrame(parent)
        else:
            return ttk.Frame(parent)
    
    def _create_label(self, parent_or_text, text=None, **kwargs):
        """Erstellt Label"""
        if text is None:
            text = parent_or_text
            parent = self.panel
        else:
            parent = parent_or_text
        
        if CTK_AVAILABLE:
            return ctk.CTkLabel(parent, text=text, **kwargs)
        else:
            return ttk.Label(parent, text=text, **kwargs)
    
    def _load_tutorials(self):
        """Lädt verfügbare Tutorials"""
        try:
            tutorials = self.tutorial_system.get_available_tutorials()
            
            self.tutorial_list.delete(0, tk.END)
            self.tutorial_data = {}
            
            for tutorial in tutorials:
                title = tutorial['title']
                tutorial_id = tutorial['id']
                
                # Zeige Status
                if tutorial.get('progress') and tutorial['progress']['status'] == 'completed':
                    title += " ✅"
                elif tutorial.get('progress') and tutorial['progress']['status'] == 'in_progress':
                    title += " 🔄"
                
                self.tutorial_list.insert(tk.END, title)
                self.tutorial_data[title] = tutorial
                
        except Exception as e:
            print(f"Tutorial Load Fehler: {e}")
    
    def _on_tutorial_select(self, event):
        """Tutorial-Auswahl Handler"""
        selection = self.tutorial_list.curselection()
        if selection:
            title = self.tutorial_list.get(selection[0])
            tutorial = self.tutorial_data.get(title)
            
            if tutorial:
                self._display_tutorial_info(tutorial)
    
    def _display_tutorial_info(self, tutorial):
        """Zeigt Tutorial-Informationen"""
        try:
            info_text = f"""Titel: {tutorial['title']}

Beschreibung: {tutorial['description']}

Typ: {tutorial['type']}
Schwierigkeit: {'⭐' * tutorial['difficulty_level']} ({tutorial['difficulty_level']}/5)
Geschätzte Dauer: {tutorial['estimated_duration']} Minuten

Lernziele:
"""
            for objective in tutorial['learning_objectives']:
                info_text += f"• {objective}\n"
            
            if tutorial['prerequisites']:
                info_text += f"\nVoraussetzungen:\n"
                for prereq in tutorial['prerequisites']:
                    info_text += f"• {prereq}\n"
            
            if tutorial.get('progress'):
                progress = tutorial['progress']
                info_text += f"\nFortschritt: {progress['percentage']:.1f}%"
                info_text += f"\nStatus: {progress['status']}"
            
            # Display content
            if CTK_AVAILABLE:
                self.tutorial_info.delete("1.0", tk.END)
                self.tutorial_info.insert("1.0", info_text)
            else:
                self.tutorial_info.delete("1.0", tk.END)
                self.tutorial_info.insert("1.0", info_text)
            
            self.current_tutorial = tutorial
            
        except Exception as e:
            print(f"Tutorial Info Display Fehler: {e}")
    
    def _start_tutorial(self):
        """Startet ausgewähltes Tutorial"""
        if self.current_tutorial:
            try:
                tutorial_id = self.current_tutorial['id']
                success = self.tutorial_system.start_tutorial(tutorial_id)
                
                if success:
                    messagebox.showinfo("Tutorial gestartet", f"Tutorial '{self.current_tutorial['title']}' wurde gestartet!")
                    self._load_tutorials()  # Refresh status
                else:
                    messagebox.showwarning("Fehler", "Tutorial konnte nicht gestartet werden. Möglicherweise fehlen Voraussetzungen.")
                    
            except Exception as e:
                messagebox.showerror("Fehler", f"Fehler beim Starten des Tutorials: {e}")
    
    def _stop_tutorial(self):
        """Stoppt aktuelles Tutorial"""
        try:
            # TODO: Implement tutorial stopping
            messagebox.showinfo("Tutorial gestoppt", "Tutorial wurde gestoppt.")
            self._load_tutorials()  # Refresh status
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Stoppen des Tutorials: {e}")


class Phase4TabManager:
    """Manager für alle Phase 4 Tabs"""
    
    def __init__(self, parent, documentation_engine, thought_stream_engine, extended_settings, tutorial_system):
        self.parent = parent
        self.documentation_engine = documentation_engine
        self.thought_stream_engine = thought_stream_engine
        self.extended_settings = extended_settings
        self.tutorial_system = tutorial_system
        
        self.notebook = None
        self.panels = {}
        
        self._create_tabs()
    
    def _create_tabs(self):
        """Erstellt Tab-Interface"""
        if CTK_AVAILABLE:
            self.notebook = ctk.CTkTabview(self.parent)
        else:
            self.notebook = ttk.Notebook(self.parent)
        
        self.notebook.pack(fill="both", expand=True)
        
        # Documentation Tab
        if CTK_AVAILABLE:
            doc_tab = self.notebook.add("📚 Dokumentation")
        else:
            doc_frame = ttk.Frame(self.notebook)
            self.notebook.add(doc_frame, text="📚 Dokumentation")
            doc_tab = doc_frame
        
        self.panels['documentation'] = DocumentationPanel(doc_tab, self.documentation_engine)
        self.panels['documentation'].panel.pack(fill="both", expand=True)
        
        # Thought Stream Tab
        if CTK_AVAILABLE:
            thought_tab = self.notebook.add("🧠 Gedankenstrom")
        else:
            thought_frame = ttk.Frame(self.notebook)
            self.notebook.add(thought_frame, text="🧠 Gedankenstrom")
            thought_tab = thought_frame
        
        self.panels['thoughts'] = ThoughtStreamPanel(thought_tab, self.thought_stream_engine)
        self.panels['thoughts'].panel.pack(fill="both", expand=True)
        
        # Extended Settings Tab
        if CTK_AVAILABLE:
            settings_tab = self.notebook.add("⚙️ Einstellungen")
        else:
            settings_frame = ttk.Frame(self.notebook)
            self.notebook.add(settings_frame, text="⚙️ Einstellungen")
            settings_tab = settings_frame
        
        self.panels['settings'] = ExtendedSettingsPanel(settings_tab, self.extended_settings)
        self.panels['settings'].panel.pack(fill="both", expand=True)
        
        # Tutorial Tab
        if CTK_AVAILABLE:
            tutorial_tab = self.notebook.add("🎓 Tutorials")
        else:
            tutorial_frame = ttk.Frame(self.notebook)
            self.notebook.add(tutorial_frame, text="🎓 Tutorials")
            tutorial_tab = tutorial_frame
        
        self.panels['tutorials'] = TutorialPanel(tutorial_tab, self.tutorial_system)
        self.panels['tutorials'].panel.pack(fill="both", expand=True)
    
    def get_panel(self, panel_name):
        """Liefert spezifisches Panel"""
        return self.panels.get(panel_name)


if __name__ == "__main__":
    # Test der Phase 4 GUI Components
    root = tk.Tk()
    root.title("Phase 4 GUI Test")
    root.geometry("1000x700")
    
    # Dummy-Engines für Test
    class DummyEngine:
        def get_component_categories(self):
            return ["AI & Intelligenz", "System", "Produktivität"]
        
        def get_system_overview(self):
            return "Test System Overview"
        
        def get_components_by_category(self, category):
            return [{"name": f"Test Component {i}", "description": f"Description {i}"} for i in range(3)]
        
        def search_functions(self, query):
            return [{"name": f"Function {query}", "description": "Test function", "category": "Test"}]
    
    dummy_engine = DummyEngine()
    
    # Test Documentation Panel
    doc_panel = DocumentationPanel(root, dummy_engine)
    doc_panel.panel.pack(fill="both", expand=True)
    
    root.mainloop()
