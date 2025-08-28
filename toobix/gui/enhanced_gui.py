"""
Toobix Enhanced GUI - Tabbed Interface
Moderne Multi-Tab-Interface mit separaten Funktionsbereichen
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import asyncio
import time
import os
from typing import Optional
from pathlib import Path

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

class EnhancedToobixGUI:
    """Erweiterte GUI mit Tabs für verschiedene Funktionsbereiche"""
    
    def __init__(self, ai_handler, speech_engine, desktop, settings):
        self.ai_handler = ai_handler
        self.speech_engine = speech_engine
        self.desktop = desktop
        self.settings = settings
        
        self.gui_config = settings.get_gui_config()
        self.root = None
        self.notebook = None
        
        # Tab-spezifische Widgets
        self.chat_display = None
        self.input_field = None
        self.commands_tree = None
        self.memory_tree = None
        self.file_tree = None
        self.system_info = None
        
        # Chat-Historie
        self.chat_history = []
        
        # File Explorer state
        self.current_directory = str(Path.home())
        self.selected_file = None
        
        print("🎨 Enhanced GUI wird initialisiert...")
        self._setup_enhanced_gui()
    
    def _setup_enhanced_gui(self):
        """Erstellt die erweiterte Multi-Tab-GUI (Thread-safe)"""
        # Prüfe ob wir im Hauptthread sind
        if threading.current_thread() != threading.main_thread():
            print("⚠️ GUI wird nicht im Hauptthread gestartet - verwende Schedule")
            # Schedule GUI creation for main thread
            self.root = None
            return
        
        # Hauptfenster
        try:
            if CTK_AVAILABLE:
                ctk.set_appearance_mode(self.gui_config['theme'])
                ctk.set_default_color_theme("blue")
                self.root = ctk.CTk()
            else:
                self.root = tk.Tk()
            
            self.root.title("Toobix AI Assistant - Enhanced Edition")
            self.root.geometry("1200x800")  # Größer für Tabs
            
            # Icon (falls vorhanden)
            try:
                self.root.iconbitmap("toobix_icon.ico")
            except:
                pass
            
            # Erstelle Tab-System
            self._create_tab_system()
            
            # Keyboard shortcuts
            self._setup_bindings()
            
            print("✅ Enhanced GUI erstellt")
            
        except Exception as e:
            print(f"❌ GUI-Fehler: {e}")
            # Fallback zu Standard-Tkinter
            try:
                self.root = tk.Tk()
                self.root.title("Toobix AI Assistant - Enhanced Edition (Fallback)")
                self.root.geometry("1200x800")
                self._create_tab_system()
                self._setup_bindings()
                print("✅ Enhanced GUI erstellt (Fallback-Modus)")
            except Exception as e2:
                print(f"❌ Kritischer GUI-Fehler: {e2}")
                self.root = None
    
    def _create_tab_system(self):
        """Erstellt das Tab-System mit verschiedenen Bereichen"""
        # Notebook (Tab-Container)
        if CTK_AVAILABLE:
            self.notebook = ctk.CTkTabview(self.root)
        else:
            self.notebook = ttk.Notebook(self.root)
        
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tab 1: Chat (Hauptfunktion)
        self._create_chat_tab()
        
        # Tab 2: Befehle & Quick Actions
        self._create_commands_tab()
        
        # Tab 3: Erinnerungen & Wissensbasis
        self._create_memory_tab()
        
        # Tab 4: Datei-Explorer mit KI
        self._create_file_explorer_tab()
        
        # Tab 5: System-Monitoring
        self._create_system_monitor_tab()
        
        # Tab 6: Git & Projekte
        self._create_git_projects_tab()
        
        # Tab 7: Automation & Tasks
        self._create_automation_tab()
    
    def _create_chat_tab(self):
        """Erstellt den Chat-Tab (Hauptfunktion)"""
        if CTK_AVAILABLE:
            chat_frame = self.notebook.add("💬 Chat")
        else:
            chat_frame = ttk.Frame(self.notebook)
            self.notebook.add(chat_frame, text="💬 Chat")
        
        # Chat-Display
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=25,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#1e1e1e" if self.gui_config['theme'] == "dark" else "white",
            fg="white" if self.gui_config['theme'] == "dark" else "black"
        )
        self.chat_display.pack(fill="both", expand=True, padx=10, pady=(10, 5))
        
        # Input-Frame
        input_frame = tk.Frame(chat_frame)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Input-Field
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg="#2d2d2d" if self.gui_config['theme'] == "dark" else "white",
            fg="white" if self.gui_config['theme'] == "dark" else "black"
        )
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Send Button
        send_button = tk.Button(
            input_frame,
            text="📤 Senden",
            command=self._on_send_message,
            bg="#0078d4",
            fg="white",
            font=("Arial", 10)
        )
        send_button.pack(side="right", padx=5)
        
        # Voice Button
        voice_button = tk.Button(
            input_frame,
            text="🎤 Sprechen",
            command=self._on_voice_input,
            bg="#005a9e",
            fg="white",
            font=("Arial", 10)
        )
        voice_button.pack(side="right")
        
        # Status-Frame
        status_frame = tk.Frame(chat_frame)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = tk.Label(
            status_frame,
            text="Bereit - Sage 'Hey Toobix' oder tippe deine Frage",
            font=("Arial", 9),
            fg="gray"
        )
        self.status_label.pack(side="left")
        
        # Begrüßungsnachricht
        self._add_message("Toobix", "🚀 Willkommen bei Toobix Enhanced! Nutze die Tabs oben für verschiedene Funktionen oder chatte hier direkt mit mir.")
    
    def _create_commands_tab(self):
        """Erstellt den Befehle-Tab mit Click-to-Execute"""
        if CTK_AVAILABLE:
            commands_frame = self.notebook.add("⚡ Befehle")
        else:
            commands_frame = ttk.Frame(self.notebook)
            self.notebook.add(commands_frame, text="⚡ Befehle")
        
        # Überschrift
        title_label = tk.Label(
            commands_frame,
            text="🎯 QUICK-BEFEHLE - Einfach anklicken!",
            font=("Arial", 14, "bold"),
            fg="#0078d4"
        )
        title_label.pack(pady=10)
        
        # Scroll-Container für Befehle
        commands_scroll = scrolledtext.ScrolledText(
            commands_frame,
            height=30,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        commands_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Befehlskategorien mit Buttons
        self._populate_commands_tab(commands_scroll)
    
    def _populate_commands_tab(self, commands_widget):
        """Füllt den Befehle-Tab mit klickbaren Befehlen"""
        commands_widget.config(state=tk.NORMAL)
        commands_widget.delete(1.0, tk.END)
        
        command_categories = {
            "🖥️ SYSTEM-BEFEHLE": [
                ("system status", "Live-Systemstatus anzeigen"),
                ("system health", "Gesundheitscheck durchführen"),
                ("analysiere system", "System-Analyse starten"),
                ("aufräumplan", "Aufräumplan erstellen"),
                ("backup erstellen", "System-Backup erstellen")
            ],
            "🔧 GIT & ENTWICKLUNG": [
                ("git scan", "Alle Git-Repositories finden"),
                ("git report", "Git-Übersichtsbericht"),
                ("git health", "Git-Repositories prüfen"),
                ("scanne projekte", "Code-Projekte finden"),
                ("finde duplikate", "Doppelte Projekte identifizieren")
            ],
            "⚙️ AUTOMATISIERUNG": [
                ("zeige tasks", "Geplante Tasks anzeigen"),
                ("scheduler status", "Task-Scheduler Status"),
                ("erstelle automation daily_cleanup", "Tägliche Aufräumung aktivieren"),
                ("erstelle automation weekly_backup", "Wöchentliches Backup aktivieren")
            ],
            "🧠 WISSENSBASIS": [
                ("zeige erinnerungen", "Alle Erinnerungen anzeigen"),
                ("vorschläge", "Personalisierte Vorschläge"),
                ("was weißt du", "Wissensbasis-Übersicht")
            ],
            "🚀 PROGRAMME": [
                ("öffne notepad", "Notepad öffnen"),
                ("öffne calculator", "Rechner öffnen"),
                ("öffne browser", "Browser öffnen"),
                ("öffne vscode", "VS Code öffnen")
            ]
        }
        
        for category, commands in command_categories.items():
            # Kategorie-Header
            commands_widget.insert(tk.END, f"\n{category}\n", "category")
            commands_widget.insert(tk.END, "=" * len(category) + "\n\n", "separator")
            
            # Befehle als klickbare Links
            for command, description in commands:
                # Button-ähnlicher Text
                button_text = f"🔹 {command}\n"
                commands_widget.insert(tk.END, button_text, f"command_{command}")
                commands_widget.insert(tk.END, f"   {description}\n\n", "description")
                
                # Tag für Klick-Event
                commands_widget.tag_bind(
                    f"command_{command}", 
                    "<Button-1>", 
                    lambda e, cmd=command: self._execute_command_from_tab(cmd)
                )
                commands_widget.tag_config(f"command_{command}", foreground="#0078d4", underline=True)
        
        # Text-Styling
        commands_widget.tag_config("category", font=("Arial", 12, "bold"), foreground="#2d5aa0")
        commands_widget.tag_config("separator", foreground="gray")
        commands_widget.tag_config("description", foreground="gray", font=("Arial", 9))
        
        commands_widget.config(state=tk.DISABLED)
    
    def _create_memory_tab(self):
        """Erstellt den Erinnerungs-Tab"""
        if CTK_AVAILABLE:
            memory_frame = self.notebook.add("🧠 Erinnerungen")
        else:
            memory_frame = ttk.Frame(self.notebook)
            self.notebook.add(memory_frame, text="🧠 Erinnerungen")
        
        # Überschrift
        title_label = tk.Label(
            memory_frame,
            text="🧠 WISSENSBASIS & ERINNERUNGEN",
            font=("Arial", 14, "bold"),
            fg="#0078d4"
        )
        title_label.pack(pady=10)
        
        # Control-Frame
        control_frame = tk.Frame(memory_frame)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        # Refresh-Button
        refresh_btn = tk.Button(
            control_frame,
            text="🔄 Aktualisieren",
            command=self._refresh_memory_tab,
            bg="#28a745",
            fg="white"
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Add Memory Button
        add_memory_btn = tk.Button(
            control_frame,
            text="➕ Erinnerung hinzufügen",
            command=self._add_memory_dialog,
            bg="#007bff",
            fg="white"
        )
        add_memory_btn.pack(side="left", padx=5)
        
        # Memory TreeView
        tree_frame = tk.Frame(memory_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side="right", fill="y")
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")
        
        # TreeView
        self.memory_tree = ttk.Treeview(
            tree_frame,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set,
            selectmode="extended"
        )
        
        # Spalten definieren
        self.memory_tree["columns"] = ("kategorie", "schluessel", "wert", "notiz", "datum")
        self.memory_tree.column("#0", width=0, stretch=False)
        self.memory_tree.column("kategorie", width=120, anchor="w")
        self.memory_tree.column("schluessel", width=150, anchor="w")
        self.memory_tree.column("wert", width=200, anchor="w")
        self.memory_tree.column("notiz", width=200, anchor="w")
        self.memory_tree.column("datum", width=120, anchor="w")
        
        # Headers
        self.memory_tree.heading("#0", text="", anchor="w")
        self.memory_tree.heading("kategorie", text="Kategorie", anchor="w")
        self.memory_tree.heading("schluessel", text="Schlüssel", anchor="w")
        self.memory_tree.heading("wert", text="Wert", anchor="w")
        self.memory_tree.heading("notiz", text="Notiz", anchor="w")
        self.memory_tree.heading("datum", text="Datum", anchor="w")
        
        self.memory_tree.pack(fill="both", expand=True)
        
        # Scrollbars verbinden
        tree_scroll_y.config(command=self.memory_tree.yview)
        tree_scroll_x.config(command=self.memory_tree.xview)
        
        # Double-click Event
        self.memory_tree.bind("<Double-1>", self._on_memory_double_click)
        
        # Initial laden
        self._refresh_memory_tab()
    
    def _create_file_explorer_tab(self):
        """Erstellt den KI-gestützten Datei-Explorer"""
        if CTK_AVAILABLE:
            explorer_frame = self.notebook.add("📁 KI-Explorer")
        else:
            explorer_frame = ttk.Frame(self.notebook)
            self.notebook.add(explorer_frame, text="📁 KI-Explorer")
        
        # Überschrift
        title_label = tk.Label(
            explorer_frame,
            text="🔍 KI-GESTÜTZTER DATEI-EXPLORER",
            font=("Arial", 14, "bold"),
            fg="#0078d4"
        )
        title_label.pack(pady=10)
        
        # Navigation-Frame
        nav_frame = tk.Frame(explorer_frame)
        nav_frame.pack(fill="x", padx=10, pady=5)
        
        # Current Path
        self.path_var = tk.StringVar(value=self.current_directory)
        path_entry = tk.Entry(nav_frame, textvariable=self.path_var, font=("Consolas", 10))
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Navigation Buttons
        up_btn = tk.Button(nav_frame, text="⬆️ Hoch", command=self._go_up_directory)
        up_btn.pack(side="right", padx=2)
        
        home_btn = tk.Button(nav_frame, text="🏠 Home", command=self._go_home_directory)
        home_btn.pack(side="right", padx=2)
        
        refresh_btn = tk.Button(nav_frame, text="🔄 Aktualisieren", command=self._refresh_file_explorer)
        refresh_btn.pack(side="right", padx=2)
        
        # Paned Window für File Tree und Info
        paned = tk.PanedWindow(explorer_frame, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # File Tree Frame
        tree_frame = tk.Frame(paned)
        paned.add(tree_frame, width=400)
        
        # File TreeView
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        
        self.file_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        self.file_tree["columns"] = ("typ", "groesse", "datum")
        self.file_tree.column("#0", width=250)
        self.file_tree.column("typ", width=80)
        self.file_tree.column("groesse", width=100)
        self.file_tree.column("datum", width=120)
        
        self.file_tree.heading("#0", text="Name", anchor="w")
        self.file_tree.heading("typ", text="Typ", anchor="w")
        self.file_tree.heading("groesse", text="Größe", anchor="w")
        self.file_tree.heading("datum", text="Geändert", anchor="w")
        
        self.file_tree.pack(fill="both", expand=True)
        tree_scroll.config(command=self.file_tree.yview)
        
        # File Info Frame
        info_frame = tk.Frame(paned)
        paned.add(info_frame, width=400)
        
        # Info Header
        info_header = tk.Label(
            info_frame,
            text="🤖 KI-DATEI-ANALYSE",
            font=("Arial", 12, "bold"),
            fg="#0078d4"
        )
        info_header.pack(pady=5)
        
        # File Info Display
        self.file_info = scrolledtext.ScrolledText(
            info_frame,
            height=20,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        self.file_info.pack(fill="both", expand=True, padx=5, pady=5)
        
        # AI Analysis Button
        analyze_btn = tk.Button(
            info_frame,
            text="🤖 KI-Analyse starten",
            command=self._analyze_selected_file,
            bg="#ff6b35",
            fg="white",
            font=("Arial", 10, "bold")
        )
        analyze_btn.pack(pady=5)
        
        # Events
        self.file_tree.bind("<<TreeviewSelect>>", self._on_file_select)
        self.file_tree.bind("<Double-1>", self._on_file_double_click)
        path_entry.bind("<Return>", self._on_path_change)
        
        # Initial laden
        self._refresh_file_explorer()
    
    def _create_system_monitor_tab(self):
        """Erstellt den System-Monitoring-Tab"""
        if CTK_AVAILABLE:
            monitor_frame = self.notebook.add("📊 System")
        else:
            monitor_frame = ttk.Frame(self.notebook)
            self.notebook.add(monitor_frame, text="📊 System")
        
        # Überschrift
        title_label = tk.Label(
            monitor_frame,
            text="📊 ECHTZEIT SYSTEM-MONITORING",
            font=("Arial", 14, "bold"),
            fg="#0078d4"
        )
        title_label.pack(pady=10)
        
        # Control Buttons
        control_frame = tk.Frame(monitor_frame)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        refresh_btn = tk.Button(
            control_frame,
            text="🔄 Aktualisieren",
            command=self._refresh_system_monitor,
            bg="#28a745",
            fg="white"
        )
        refresh_btn.pack(side="left", padx=5)
        
        health_check_btn = tk.Button(
            control_frame,
            text="🏥 Health Check",
            command=self._run_health_check,
            bg="#dc3545",
            fg="white"
        )
        health_check_btn.pack(side="left", padx=5)
        
        auto_refresh_var = tk.BooleanVar()
        auto_refresh_cb = tk.Checkbutton(
            control_frame,
            text="🔄 Auto-Refresh (30s)",
            variable=auto_refresh_var,
            command=lambda: self._toggle_auto_refresh(auto_refresh_var.get())
        )
        auto_refresh_cb.pack(side="left", padx=20)
        
        # System Info Display
        self.system_info = scrolledtext.ScrolledText(
            monitor_frame,
            height=30,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.system_info.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Initial laden
        self._refresh_system_monitor()
    
    def _create_git_projects_tab(self):
        """Erstellt den Git & Projekte Tab"""
        if CTK_AVAILABLE:
            git_frame = self.notebook.add("🔧 Git & Projekte")
        else:
            git_frame = ttk.Frame(self.notebook)
            self.notebook.add(git_frame, text="🔧 Git & Projekte")
        
        # Wird später implementiert
        placeholder = tk.Label(
            git_frame,
            text="🔧 Git & Projekte Tab\n(Wird implementiert...)",
            font=("Arial", 14),
            fg="gray"
        )
        placeholder.pack(expand=True)
    
    def _create_automation_tab(self):
        """Erstellt den Automation Tab"""
        if CTK_AVAILABLE:
            auto_frame = self.notebook.add("⚙️ Automation")
        else:
            auto_frame = ttk.Frame(self.notebook)
            self.notebook.add(auto_frame, text="⚙️ Automation")
        
        # Wird später implementiert
        placeholder = tk.Label(
            auto_frame,
            text="⚙️ Automation & Tasks Tab\n(Wird implementiert...)",
            font=("Arial", 14),
            fg="gray"
        )
        placeholder.pack(expand=True)
    
    def _setup_bindings(self):
        """Setzt Tastatur-Shortcuts"""
        self.root.bind('<Return>', lambda e: self._on_send_message() if self.input_field and self.input_field.focus_get() == self.input_field else None)
        self.root.bind('<F1>', lambda e: self._on_voice_input())
        self.root.bind('<Escape>', lambda e: self.input_field.focus() if self.input_field else None)
    
    def _execute_command_from_tab(self, command):
        """Führt Befehl aus dem Befehle-Tab aus"""
        # Wechsle zum Chat-Tab
        if CTK_AVAILABLE:
            self.notebook.set("💬 Chat")
        else:
            self.notebook.select(0)  # Chat ist der erste Tab
        
        # Setze Befehl ins Input-Feld
        if self.input_field:
            self.input_field.delete(0, tk.END)
            self.input_field.insert(0, command)
            
        # Führe Befehl aus
        self._on_send_message()
    
    def _add_memory_dialog(self):
        """Dialog zum Hinzufügen einer Erinnerung"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Neue Erinnerung hinzufügen")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Felder
        tk.Label(dialog, text="Kategorie:", font=("Arial", 10, "bold")).pack(pady=5)
        kategorie_entry = tk.Entry(dialog, width=50)
        kategorie_entry.pack(pady=5)
        
        tk.Label(dialog, text="Schlüssel:", font=("Arial", 10, "bold")).pack(pady=5)
        schluessel_entry = tk.Entry(dialog, width=50)
        schluessel_entry.pack(pady=5)
        
        tk.Label(dialog, text="Wert:", font=("Arial", 10, "bold")).pack(pady=5)
        wert_entry = tk.Entry(dialog, width=50)
        wert_entry.pack(pady=5)
        
        tk.Label(dialog, text="Notiz (optional):", font=("Arial", 10, "bold")).pack(pady=5)
        notiz_text = tk.Text(dialog, width=50, height=4)
        notiz_text.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def save_memory():
            kategorie = kategorie_entry.get().strip()
            schluessel = schluessel_entry.get().strip()
            wert = wert_entry.get().strip()
            notiz = notiz_text.get(1.0, tk.END).strip()
            
            if kategorie and schluessel and wert:
                result = self.ai_handler.knowledge_base.remember_fact(kategorie, schluessel, wert, notiz)
                messagebox.showinfo("Erfolg", result)
                self._refresh_memory_tab()
                dialog.destroy()
            else:
                messagebox.showerror("Fehler", "Kategorie, Schlüssel und Wert sind erforderlich!")
        
        tk.Button(button_frame, text="💾 Speichern", command=save_memory, bg="#007bff", fg="white").pack(side="left", padx=5)
        tk.Button(button_frame, text="❌ Abbrechen", command=dialog.destroy).pack(side="left", padx=5)
    
    def _refresh_memory_tab(self):
        """Aktualisiert den Erinnerungs-Tab"""
        if not self.memory_tree:
            return
            
        # Lösche alte Einträge
        for item in self.memory_tree.get_children():
            self.memory_tree.delete(item)
        
        try:
            # Lade Erinnerungen von der KnowledgeBase
            knowledge = self.ai_handler.knowledge_base.knowledge
            personal_notes = knowledge.get('personal_notes', {})
            
            for kategorie, items in personal_notes.items():
                for schluessel, data in items.items():
                    if isinstance(data, dict):
                        wert = str(data.get('value', ''))
                        notiz = data.get('note', '')
                        datum = data.get('datetime', '')[:10] if data.get('datetime') else ''
                    else:
                        wert = str(data)
                        notiz = ''
                        datum = ''
                    
                    self.memory_tree.insert(
                        "",
                        "end",
                        values=(kategorie, schluessel, wert, notiz, datum)
                    )
        
        except Exception as e:
            print(f"Fehler beim Laden der Erinnerungen: {e}")
    
    def _refresh_file_explorer(self):
        """Aktualisiert den Datei-Explorer"""
        if not self.file_tree:
            return
            
        # Lösche alte Einträge
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        try:
            current_path = Path(self.current_directory)
            
            # Übergeordneter Ordner (falls nicht Root)
            if current_path.parent != current_path:
                self.file_tree.insert(
                    "",
                    "end",
                    text="📁 ..",
                    values=("Ordner", "", ""),
                    tags=("parent",)
                )
            
            # Ordner zuerst
            folders = []
            files = []
            
            for item in current_path.iterdir():
                try:
                    if item.is_dir():
                        folders.append(item)
                    else:
                        files.append(item)
                except PermissionError:
                    continue
            
            # Sortiere
            folders.sort(key=lambda x: x.name.lower())
            files.sort(key=lambda x: x.name.lower())
            
            # Füge Ordner hinzu
            for folder in folders:
                try:
                    stat = folder.stat()
                    modified = time.strftime("%d.%m.%Y %H:%M", time.localtime(stat.st_mtime))
                    
                    self.file_tree.insert(
                        "",
                        "end",
                        text=f"📁 {folder.name}",
                        values=("Ordner", "", modified),
                        tags=("folder",)
                    )
                except:
                    self.file_tree.insert(
                        "",
                        "end",
                        text=f"📁 {folder.name}",
                        values=("Ordner", "", ""),
                        tags=("folder",)
                    )
            
            # Füge Dateien hinzu
            for file in files:
                try:
                    stat = file.stat()
                    size = self._format_file_size(stat.st_size)
                    modified = time.strftime("%d.%m.%Y %H:%M", time.localtime(stat.st_mtime))
                    
                    # Icon basierend auf Dateierweiterung
                    icon = self._get_file_icon(file.suffix.lower())
                    
                    self.file_tree.insert(
                        "",
                        "end",
                        text=f"{icon} {file.name}",
                        values=("Datei", size, modified),
                        tags=("file",)
                    )
                except:
                    icon = self._get_file_icon("")
                    self.file_tree.insert(
                        "",
                        "end",
                        text=f"{icon} {file.name}",
                        values=("Datei", "", ""),
                        tags=("file",)
                    )
            
            # Update Path
            self.path_var.set(str(current_path))
            
        except Exception as e:
            print(f"Fehler beim Laden des Verzeichnisses: {e}")
    
    def _format_file_size(self, size_bytes):
        """Formatiert Dateigröße"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def _get_file_icon(self, extension):
        """Gibt Icon für Dateierweiterung zurück"""
        icons = {
            '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨',
            '.txt': '📄', '.md': '📝', '.pdf': '📕', '.doc': '📘',
            '.docx': '📘', '.xls': '📊', '.xlsx': '📊', '.ppt': '📺',
            '.pptx': '📺', '.zip': '📦', '.rar': '📦', '.7z': '📦',
            '.mp3': '🎵', '.mp4': '🎬', '.avi': '🎬', '.jpg': '🖼️',
            '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.exe': '⚙️',
            '.msi': '📦', '.json': '📋', '.xml': '📋', '.csv': '📊'
        }
        
        return icons.get(extension, '📄')
    
    def _on_file_select(self, event):
        """Datei ausgewählt"""
        selection = self.file_tree.selection()
        if selection:
            item = self.file_tree.item(selection[0])
            filename = item['text']
            
            # Entferne Icon von Filename
            if filename.startswith('📁') or any(filename.startswith(icon) for icon in ['🐍', '📜', '🌐', '🎨', '📄', '📝', '📕', '📘', '📊', '📺', '📦', '🎵', '🎬', '🖼️', '⚙️', '📋']):
                filename = filename[2:]  # Entferne Icon und Leerzeichen
            
            if filename == "..":
                return
                
            file_path = Path(self.current_directory) / filename
            self.selected_file = str(file_path)
            
            # Zeige Datei-Info
            self._show_file_info(file_path)
    
    def _show_file_info(self, file_path):
        """Zeigt Datei-Informationen an"""
        if not self.file_info:
            return
            
        self.file_info.delete(1.0, tk.END)
        
        try:
            if file_path.is_file():
                stat = file_path.stat()
                
                info = f"📄 DATEI-INFORMATIONEN\n"
                info += "=" * 30 + "\n\n"
                info += f"📁 Name: {file_path.name}\n"
                info += f"📍 Pfad: {file_path}\n"
                info += f"📏 Größe: {self._format_file_size(stat.st_size)}\n"
                info += f"📅 Erstellt: {time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(stat.st_ctime))}\n"
                info += f"✏️ Geändert: {time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(stat.st_mtime))}\n"
                info += f"🔐 Rechte: {oct(stat.st_mode)[-3:]}\n\n"
                
                # Dateierweiterung und Typ
                ext = file_path.suffix.lower()
                if ext:
                    info += f"🏷️ Erweiterung: {ext}\n"
                    info += f"📋 Typ: {self._get_file_type_description(ext)}\n\n"
                
                # Preview für Text-Dateien
                if ext in ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.xml', '.csv'] and stat.st_size < 10000:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            preview = f.read(500)
                            info += "👁️ VORSCHAU:\n"
                            info += "-" * 20 + "\n"
                            info += preview
                            if len(preview) == 500:
                                info += "\n... (gekürzt)"
                    except:
                        info += "❌ Vorschau nicht verfügbar"
                
                self.file_info.insert(1.0, info)
                
            elif file_path.is_dir():
                try:
                    items = list(file_path.iterdir())
                    folders = [item for item in items if item.is_dir()]
                    files = [item for item in items if item.is_file()]
                    
                    info = f"📁 ORDNER-INFORMATIONEN\n"
                    info += "=" * 30 + "\n\n"
                    info += f"📁 Name: {file_path.name}\n"
                    info += f"📍 Pfad: {file_path}\n"
                    info += f"📊 Inhalt: {len(folders)} Ordner, {len(files)} Dateien\n"
                    info += f"📅 Geändert: {time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(file_path.stat().st_mtime))}\n\n"
                    
                    if len(items) <= 20:
                        info += "📋 INHALT:\n"
                        info += "-" * 20 + "\n"
                        for item in sorted(items, key=lambda x: (x.is_file(), x.name.lower())):
                            icon = "📁" if item.is_dir() else self._get_file_icon(item.suffix.lower())
                            info += f"{icon} {item.name}\n"
                    else:
                        info += f"📋 INHALT: (zu viele Elemente - {len(items)} gesamt)\n"
                    
                    self.file_info.insert(1.0, info)
                    
                except PermissionError:
                    self.file_info.insert(1.0, "❌ Zugriff verweigert")
                    
        except Exception as e:
            self.file_info.insert(1.0, f"❌ Fehler beim Laden der Datei-Info: {e}")
    
    def _get_file_type_description(self, extension):
        """Gibt Beschreibung für Dateierweiterung zurück"""
        descriptions = {
            '.py': 'Python-Skript',
            '.js': 'JavaScript-Datei',
            '.html': 'HTML-Dokument',
            '.css': 'CSS-Stylesheet',
            '.txt': 'Text-Datei',
            '.md': 'Markdown-Dokument',
            '.pdf': 'PDF-Dokument',
            '.doc': 'Word-Dokument',
            '.docx': 'Word-Dokument',
            '.xls': 'Excel-Tabelle',
            '.xlsx': 'Excel-Tabelle',
            '.json': 'JSON-Daten',
            '.xml': 'XML-Daten',
            '.csv': 'CSV-Tabelle'
        }
        
        return descriptions.get(extension, 'Unbekannt')
    
    def _analyze_selected_file(self):
        """KI-Analyse der ausgewählten Datei"""
        if not self.selected_file:
            messagebox.showwarning("Warnung", "Bitte wähle zuerst eine Datei aus!")
            return
        
        try:
            file_path = Path(self.selected_file)
            
            # Erstelle KI-Analyse-Prompt
            analysis_prompt = f"Analysiere diese Datei für mich:\n\n"
            analysis_prompt += f"Dateiname: {file_path.name}\n"
            analysis_prompt += f"Pfad: {file_path}\n"
            analysis_prompt += f"Erweiterung: {file_path.suffix}\n\n"
            
            # Für Text-Dateien: Inhalt hinzufügen
            if file_path.suffix.lower() in ['.txt', '.py', '.js', '.html', '.css', '.md', '.json'] and file_path.stat().st_size < 5000:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1000)  # Erste 1000 Zeichen
                        analysis_prompt += f"Inhalt (Auszug):\n{content}\n\n"
                except:
                    pass
            
            analysis_prompt += "Bitte analysiere:\n"
            analysis_prompt += "1. Was ist das für eine Datei?\n"
            analysis_prompt += "2. Was macht sie (falls Code)?\n" 
            analysis_prompt += "3. Ist sie wichtig/nützlich?\n"
            analysis_prompt += "4. Empfehlungen für Verbesserungen?\n"
            analysis_prompt += "5. Sicherheitsaspekte?"
            
            # Wechsle zum Chat-Tab und führe Analyse aus
            if CTK_AVAILABLE:
                self.notebook.set("💬 Chat")
            else:
                self.notebook.select(0)
            
            # Füge Prompt zum Chat hinzu
            self._add_message("Du", f"🔍 KI-Analyse für: {file_path.name}")
            
            # Starte Analyse in separatem Thread
            threading.Thread(
                target=self._run_ai_analysis,
                args=(analysis_prompt,),
                daemon=True
            ).start()
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler bei der KI-Analyse: {e}")
    
    def _run_ai_analysis(self, prompt):
        """Führt KI-Analyse im Hintergrund aus"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                self.ai_handler.get_response(prompt)
            )
            
            # Antwort im Chat anzeigen
            self.root.after(0, lambda: self._add_message("Toobix (KI-Analyse)", response))
            
            # TTS
            if response:
                self.speech_engine.speak(f"KI-Analyse abgeschlossen für die ausgewählte Datei.", wait=False)
            
        except Exception as e:
            error_msg = f"❌ Fehler bei der KI-Analyse: {e}"
            self.root.after(0, lambda: self._add_message("Toobix", error_msg))
    
    def _refresh_system_monitor(self):
        """Aktualisiert das System-Monitoring"""
        if not self.system_info:
            return
            
        try:
            report = self.ai_handler.system_monitor.generate_system_report()
            
            self.system_info.delete(1.0, tk.END)
            self.system_info.insert(1.0, report)
            
        except Exception as e:
            self.system_info.delete(1.0, tk.END)
            self.system_info.insert(1.0, f"❌ Fehler beim System-Monitoring: {e}")
    
    def _run_health_check(self):
        """Führt System-Health-Check aus"""
        try:
            health = self.ai_handler.system_monitor.check_system_health()
            
            # Zeige Health-Check-Ergebnis in Dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("System Health Check")
            dialog.geometry("500x400")
            dialog.transient(self.root)
            
            # Status-Header
            status_colors = {'excellent': '#28a745', 'good': '#ffc107', 'warning': '#fd7e14', 'critical': '#dc3545'}
            status_color = status_colors.get(health['status'], '#6c757d')
            
            header = tk.Label(
                dialog,
                text=f"🏥 SYSTEM-GESUNDHEIT: {health['status'].upper()}",
                font=("Arial", 14, "bold"),
                fg=status_color
            )
            header.pack(pady=10)
            
            # Details
            details = scrolledtext.ScrolledText(dialog, height=15, wrap=tk.WORD)
            details.pack(fill="both", expand=True, padx=10, pady=10)
            
            result = f"Status: {health['status']}\n"
            result += f"Zusammenfassung: {health['summary']}\n\n"
            
            if health['alerts']:
                result += "⚠️ WARNUNGEN:\n"
                for alert in health['alerts']:
                    result += f"• {alert}\n"
                result += "\n"
            
            if health['recommendations']:
                result += "💡 EMPFEHLUNGEN:\n"
                for rec in health['recommendations']:
                    result += f"• {rec}\n"
            
            details.insert(1.0, result)
            details.config(state=tk.DISABLED)
            
            # Close Button
            tk.Button(dialog, text="✅ OK", command=dialog.destroy, bg="#007bff", fg="white").pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Health-Check: {e}")
    
    def _toggle_auto_refresh(self, enabled):
        """Togglet Auto-Refresh für System-Monitor"""
        # Wird später implementiert
        pass
    
    # Navigation methods für File Explorer
    def _go_up_directory(self):
        """Geht eine Ebene höher"""
        current = Path(self.current_directory)
        if current.parent != current:
            self.current_directory = str(current.parent)
            self._refresh_file_explorer()
    
    def _go_home_directory(self):
        """Geht zum Home-Verzeichnis"""
        self.current_directory = str(Path.home())
        self._refresh_file_explorer()
    
    def _on_path_change(self, event):
        """Pfad manuell geändert"""
        new_path = self.path_var.get()
        if Path(new_path).exists() and Path(new_path).is_dir():
            self.current_directory = new_path
            self._refresh_file_explorer()
        else:
            messagebox.showerror("Fehler", "Ungültiger Pfad!")
            self.path_var.set(self.current_directory)
    
    def _on_file_double_click(self, event):
        """Doppelklick auf Datei/Ordner"""
        selection = self.file_tree.selection()
        if not selection:
            return
            
        item = self.file_tree.item(selection[0])
        filename = item['text']
        
        # Entferne Icon
        if filename.startswith('📁') or any(filename.startswith(icon) for icon in ['🐍', '📜', '🌐', '🎨', '📄', '📝', '📕', '📘', '📊', '📺', '📦', '🎵', '🎬', '🖼️', '⚙️', '📋']):
            filename = filename[2:]
        
        if filename == "..":
            self._go_up_directory()
            return
        
        file_path = Path(self.current_directory) / filename
        
        if file_path.is_dir():
            self.current_directory = str(file_path)
            self._refresh_file_explorer()
        else:
            # Öffne Datei mit Standard-Programm
            try:
                os.startfile(str(file_path))
            except:
                messagebox.showwarning("Warnung", "Datei konnte nicht geöffnet werden")
    
    def _on_memory_double_click(self, event):
        """Doppelklick auf Erinnerung"""
        selection = self.memory_tree.selection()
        if selection:
            item = self.memory_tree.item(selection[0])
            values = item['values']
            
            # Zeige Details in Dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Erinnerung Details")
            dialog.geometry("400x300")
            dialog.transient(self.root)
            
            details_text = scrolledtext.ScrolledText(dialog, wrap=tk.WORD)
            details_text.pack(fill="both", expand=True, padx=10, pady=10)
            
            details = f"Kategorie: {values[0]}\n"
            details += f"Schlüssel: {values[1]}\n"
            details += f"Wert: {values[2]}\n"
            details += f"Notiz: {values[3]}\n"
            details += f"Datum: {values[4]}\n"
            
            details_text.insert(1.0, details)
            details_text.config(state=tk.DISABLED)
            
            tk.Button(dialog, text="✅ OK", command=dialog.destroy).pack(pady=5)
    
    # Standard GUI-Methods (übernommen von der alten GUI)
    def _add_message(self, sender: str, message: str):
        """Fügt Nachricht zum Chat hinzu"""
        if not self.chat_display:
            return
            
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.see(tk.END)
        
        # Zu Historie hinzufügen
        self.chat_history.append({
            'timestamp': timestamp,
            'sender': sender,
            'message': message
        })
    
    def _on_send_message(self):
        """Sendet Nachricht"""
        if not self.input_field:
            return
            
        message = self.input_field.get().strip()
        if not message:
            return
        
        self.input_field.delete(0, tk.END)
        self._add_message("Du", message)
        
        # Verarbeite in separatem Thread
        threading.Thread(
            target=self._process_message,
            args=(message,),
            daemon=True
        ).start()
    
    def _process_message(self, message: str):
        """Verarbeitet Nachricht (gleich wie alte GUI)"""
        try:
            # Status anzeigen
            self.root.after(0, lambda: self._update_status("🤔 Denke nach..."))
            
            # System-Kommandos erkennen
            from ..gui.main_window import ToobixGUI
            temp_gui = ToobixGUI(self.ai_handler, self.speech_engine, self.desktop, self.settings)
            system_response = temp_gui._handle_system_commands(message)
            
            if system_response:
                # Logge in KnowledgeBase
                self.ai_handler.knowledge_base.log_interaction(message, system_response, {'type': 'system_command'})
                
                self.root.after(0, lambda: self._add_message("Toobix", system_response))
                if system_response:
                    self.speech_engine.speak(system_response, wait=False)
                self.root.after(0, lambda: self._update_status("Bereit"))
                return
            
            # KI-Antwort
            user_context = self.ai_handler.knowledge_base.create_user_context()
            enhanced_prompt = f"[Benutzer-Kontext: {user_context}]\n\nFrage: {message}"
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                self.ai_handler.get_response(enhanced_prompt)
            )
            
            # Logge Interaktion
            self.ai_handler.knowledge_base.log_interaction(message, response, {
                'type': 'ai_chat',
                'user_context': user_context
            })
            
            self.root.after(0, lambda: self._add_message("Toobix", response))
            
            if response:
                self.speech_engine.speak(response, wait=False)
            
        except Exception as e:
            error_msg = f"❌ Entschuldigung, es gab einen Fehler: {e}"
            self.ai_handler.knowledge_base.log_interaction(message, error_msg, {'type': 'error'})
            self.root.after(0, lambda: self._add_message("Toobix", error_msg))
        
        finally:
            self.root.after(0, lambda: self._update_status("Bereit"))
    
    def _on_voice_input(self):
        """Voice-Input (vereinfacht)"""
        try:
            # Placeholder - würde die Speech-Engine verwenden
            messagebox.showinfo("Voice Input", "Voice-Input wird in Enhanced GUI bald verfügbar!")
        except:
            pass
    
    def _update_status(self, status: str):
        """Aktualisiert Status"""
        if self.status_label:
            self.status_label.config(text=status)
    
    def run(self):
        """Startet die GUI"""
        print("🎨 Enhanced GUI gestartet")
        self.root.mainloop()
    
    def close(self):
        """Schließt die GUI"""
        if self.root:
            self.root.destroy()
