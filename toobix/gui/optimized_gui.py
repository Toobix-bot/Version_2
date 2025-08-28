"""
Toobix Optimized GUI - Robuste, Thread-sichere GUI
Komplett überarbeitete GUI mit verbesserter Stabilität
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import asyncio
import time
import os
from typing import Optional, Dict, Any, List
from pathlib import Path

class OptimizedToobixGUI:
    """Optimierte, robuste GUI für Toobix"""
    
    def __init__(self, ai_handler, speech_engine, desktop, settings):
        self.ai_handler = ai_handler
        self.speech_engine = speech_engine
        self.desktop = desktop
        self.settings = settings
        
        # GUI State
        self.root = None
        self.notebook = None
        self.is_running = False
        self.gui_ready = False
        
        # Widgets
        self.chat_display = None
        self.input_field = None
        self.status_label = None
        
        # Threading
        self.gui_lock = threading.Lock()
        
        print("🎨 Optimierte GUI wird initialisiert...")
        self._setup_gui()
    
    def _setup_gui(self):
        """Erstellt die optimierte GUI (Thread-safe)"""
        try:
            # Hauptfenster
            self.root = tk.Tk()
            self.root.title("Toobix AI Assistant - Optimized")
            self.root.geometry("1000x700")
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            
            # Erstelle Tab-System
            self._create_notebook()
            
            # Status-Bar
            self._create_status_bar()
            
            # Keyboard Bindings
            self._setup_bindings()
            
            self.gui_ready = True
            print("✅ Optimierte GUI erstellt")
            
        except Exception as e:
            print(f"❌ GUI-Setup-Fehler: {e}")
            self.root = None
    
    def _create_notebook(self):
        """Erstellt das Tab-System"""
        try:
            self.notebook = ttk.Notebook(self.root)
            self.notebook.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Chat Tab
            self._create_chat_tab()
            
            # Commands Tab
            self._create_commands_tab()
            
            # System Tab
            self._create_system_tab()
            
            # Files Tab
            self._create_files_tab()
            
        except Exception as e:
            print(f"❌ Notebook-Fehler: {e}")
    
    def _create_chat_tab(self):
        """Erstellt den Chat-Tab"""
        try:
            chat_frame = ttk.Frame(self.notebook)
            self.notebook.add(chat_frame, text="💬 Chat")
            
            # Chat-Display
            self.chat_display = scrolledtext.ScrolledText(
                chat_frame,
                height=20,
                wrap=tk.WORD,
                font=("Consolas", 10),
                bg="#f0f0f0",
                fg="black"
            )
            self.chat_display.pack(fill="both", expand=True, padx=10, pady=(10, 5))
            
            # Input-Frame
            input_frame = ttk.Frame(chat_frame)
            input_frame.pack(fill="x", padx=10, pady=5)
            
            # Input-Field
            self.input_field = ttk.Entry(input_frame, font=("Arial", 11))
            self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 5))
            
            # Send Button
            send_btn = ttk.Button(input_frame, text="📤 Senden", command=self._on_send_message)
            send_btn.pack(side="right", padx=5)
            
            # Voice Button
            voice_btn = ttk.Button(input_frame, text="🎤 Sprechen", command=self._on_voice_input)
            voice_btn.pack(side="right")
            
            # Begrüßung
            self._add_message("Toobix", "🚀 Willkommen bei Toobix Optimized! Ich bin bereit für deine Fragen.")
            
        except Exception as e:
            print(f"❌ Chat-Tab-Fehler: {e}")
    
    def _create_commands_tab(self):
        """Erstellt den Befehle-Tab"""
        try:
            commands_frame = ttk.Frame(self.notebook)
            self.notebook.add(commands_frame, text="⚡ Befehle")
            
            # Header
            header = ttk.Label(commands_frame, text="🎯 QUICK-BEFEHLE", font=("Arial", 14, "bold"))
            header.pack(pady=10)
            
            # Commands-Container
            commands_container = ttk.Frame(commands_frame)
            commands_container.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Befehlskategorien
            self._create_command_buttons(commands_container)
            
        except Exception as e:
            print(f"❌ Commands-Tab-Fehler: {e}")
    
    def _create_command_buttons(self, parent):
        """Erstellt Befehlsbuttons"""
        try:
            # System Commands
            system_frame = ttk.LabelFrame(parent, text="🖥️ System", padding=10)
            system_frame.pack(fill="x", pady=5)
            
            ttk.Button(system_frame, text="System Status", 
                      command=lambda: self._execute_command("system status")).pack(side="left", padx=5)
            ttk.Button(system_frame, text="Health Check", 
                      command=lambda: self._execute_command("system health")).pack(side="left", padx=5)
            ttk.Button(system_frame, text="Aufräumplan", 
                      command=lambda: self._execute_command("aufräumplan")).pack(side="left", padx=5)
            
            # Git Commands
            git_frame = ttk.LabelFrame(parent, text="🔧 Git & Projekte", padding=10)
            git_frame.pack(fill="x", pady=5)
            
            ttk.Button(git_frame, text="Git Scan", 
                      command=lambda: self._execute_command("git scan")).pack(side="left", padx=5)
            ttk.Button(git_frame, text="Git Report", 
                      command=lambda: self._execute_command("git report")).pack(side="left", padx=5)
            ttk.Button(git_frame, text="Projekte finden", 
                      command=lambda: self._execute_command("scanne projekte")).pack(side="left", padx=5)
            
            # Knowledge Commands
            knowledge_frame = ttk.LabelFrame(parent, text="🧠 Wissen", padding=10)
            knowledge_frame.pack(fill="x", pady=5)
            
            ttk.Button(knowledge_frame, text="Erinnerungen zeigen", 
                      command=lambda: self._execute_command("zeige erinnerungen")).pack(side="left", padx=5)
            ttk.Button(knowledge_frame, text="Vorschläge", 
                      command=lambda: self._execute_command("vorschläge")).pack(side="left", padx=5)
            
        except Exception as e:
            print(f"❌ Command-Buttons-Fehler: {e}")
    
    def _create_system_tab(self):
        """Erstellt den System-Tab"""
        try:
            system_frame = ttk.Frame(self.notebook)
            self.notebook.add(system_frame, text="📊 System")
            
            # Header
            header = ttk.Label(system_frame, text="📊 SYSTEM-MONITORING", font=("Arial", 14, "bold"))
            header.pack(pady=10)
            
            # Refresh Button
            refresh_btn = ttk.Button(system_frame, text="🔄 Aktualisieren", command=self._refresh_system_info)
            refresh_btn.pack(pady=5)
            
            # System Info Display
            self.system_info = scrolledtext.ScrolledText(
                system_frame,
                height=25,
                wrap=tk.WORD,
                font=("Consolas", 9)
            )
            self.system_info.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Initial load
            self._refresh_system_info()
            
        except Exception as e:
            print(f"❌ System-Tab-Fehler: {e}")
    
    def _create_files_tab(self):
        """Erstellt den Datei-Tab"""
        try:
            files_frame = ttk.Frame(self.notebook)
            self.notebook.add(files_frame, text="📁 Dateien")
            
            # Header
            header = ttk.Label(files_frame, text="📁 DATEI-EXPLORER", font=("Arial", 14, "bold"))
            header.pack(pady=10)
            
            # Path Frame
            path_frame = ttk.Frame(files_frame)
            path_frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(path_frame, text="Pfad:").pack(side="left")
            self.path_var = tk.StringVar(value=str(Path.home()))
            path_entry = ttk.Entry(path_frame, textvariable=self.path_var)
            path_entry.pack(side="left", fill="x", expand=True, padx=5)
            
            ttk.Button(path_frame, text="🔄", command=self._browse_files).pack(side="right")
            
            # File List
            self.file_listbox = tk.Listbox(files_frame, height=15)
            self.file_listbox.pack(fill="both", expand=True, padx=10, pady=10)
            
            # File Info
            self.file_info_text = tk.Text(files_frame, height=5, wrap=tk.WORD)
            self.file_info_text.pack(fill="x", padx=10, pady=(0, 10))
            
            # Events
            self.file_listbox.bind("<<ListboxSelect>>", self._on_file_select)
            
            # Initial load
            self._browse_files()
            
        except Exception as e:
            print(f"❌ Files-Tab-Fehler: {e}")
    
    def _create_status_bar(self):
        """Erstellt die Status-Bar"""
        try:
            status_frame = ttk.Frame(self.root)
            status_frame.pack(fill="x", side="bottom")
            
            self.status_label = ttk.Label(status_frame, text="Bereit - Toobix ist einsatzbereit!", relief="sunken")
            self.status_label.pack(fill="x", padx=5, pady=2)
            
        except Exception as e:
            print(f"❌ Status-Bar-Fehler: {e}")
    
    def _setup_bindings(self):
        """Keyboard Shortcuts"""
        if self.root and self.input_field:
            self.root.bind('<Return>', lambda e: self._on_send_message() if self.input_field.focus_get() == self.input_field else None)
            self.root.bind('<F1>', lambda e: self._on_voice_input())
            self.root.bind('<Escape>', lambda e: self.input_field.focus() if self.input_field else None)
    
    def _execute_command(self, command: str):
        """Führt Befehl aus dem Commands-Tab aus"""
        try:
            # Wechsle zum Chat-Tab
            self.notebook.select(0)
            
            # Setze Befehl ins Input-Feld
            if self.input_field:
                self.input_field.delete(0, tk.END)
                self.input_field.insert(0, command)
                
            # Führe Befehl aus
            self._on_send_message()
            
        except Exception as e:
            print(f"❌ Command-Execution-Fehler: {e}")
    
    def _refresh_system_info(self):
        """Aktualisiert System-Info"""
        try:
            if hasattr(self, 'system_info') and self.system_info:
                self.system_info.delete(1.0, tk.END)
                
                # System-Bericht generieren
                if hasattr(self.ai_handler, 'system_monitor'):
                    report = self.ai_handler.system_monitor.generate_system_report()
                    self.system_info.insert(1.0, report)
                else:
                    # Fallback-System-Info
                    import psutil
                    info = f"📊 SYSTEM-ÜBERSICHT\n{'='*50}\n\n"
                    info += f"💻 CPU: {psutil.cpu_percent()}%\n"
                    info += f"🧠 RAM: {psutil.virtual_memory().percent}%\n"
                    info += f"💾 Disk: {psutil.disk_usage('/').percent}%\n"
                    info += f"🕒 Zeit: {time.strftime('%d.%m.%Y %H:%M:%S')}\n"
                    self.system_info.insert(1.0, info)
                    
        except Exception as e:
            if hasattr(self, 'system_info') and self.system_info:
                self.system_info.delete(1.0, tk.END)
                self.system_info.insert(1.0, f"❌ Fehler beim Laden der System-Info: {e}")
    
    def _browse_files(self):
        """Durchsucht Dateien"""
        try:
            if hasattr(self, 'file_listbox') and self.file_listbox:
                self.file_listbox.delete(0, tk.END)
                
                current_path = Path(self.path_var.get())
                if current_path.exists() and current_path.is_dir():
                    try:
                        items = list(current_path.iterdir())
                        
                        # Sortiere: Ordner zuerst, dann Dateien
                        folders = [item for item in items if item.is_dir()]
                        files = [item for item in items if item.is_file()]
                        
                        folders.sort(key=lambda x: x.name.lower())
                        files.sort(key=lambda x: x.name.lower())
                        
                        # Übergeordneter Ordner
                        if current_path.parent != current_path:
                            self.file_listbox.insert(tk.END, "📁 ..")
                        
                        # Ordner
                        for folder in folders:
                            self.file_listbox.insert(tk.END, f"📁 {folder.name}")
                        
                        # Dateien
                        for file in files:
                            icon = self._get_file_icon(file.suffix.lower())
                            self.file_listbox.insert(tk.END, f"{icon} {file.name}")
                            
                    except PermissionError:
                        self.file_listbox.insert(tk.END, "❌ Zugriff verweigert")
                        
                else:
                    self.file_listbox.insert(tk.END, "❌ Ungültiger Pfad")
                    
        except Exception as e:
            print(f"❌ File-Browse-Fehler: {e}")
    
    def _get_file_icon(self, extension: str) -> str:
        """Gibt Icon für Dateierweiterung zurück"""
        icons = {
            '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨',
            '.txt': '📄', '.md': '📝', '.pdf': '📕', '.doc': '📘',
            '.jpg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.mp3': '🎵',
            '.mp4': '🎬', '.zip': '📦', '.exe': '⚙️', '.json': '📋'
        }
        return icons.get(extension, '📄')
    
    def _on_file_select(self, event):
        """Datei ausgewählt"""
        try:
            if hasattr(self, 'file_listbox') and hasattr(self, 'file_info_text'):
                selection = self.file_listbox.curselection()
                if selection:
                    filename = self.file_listbox.get(selection[0])
                    
                    # Entferne Icon
                    if filename.startswith(('📁', '🐍', '📜', '🌐', '🎨', '📄', '📝', '📕', '📘', '🖼️', '🎵', '🎬', '📦', '⚙️', '📋')):
                        filename = filename[2:]  # Entferne Icon und Leerzeichen
                    
                    current_path = Path(self.path_var.get())
                    file_path = current_path / filename
                    
                    # Zeige Datei-Info
                    self.file_info_text.delete(1.0, tk.END)
                    
                    if filename == "..":
                        self.file_info_text.insert(1.0, "📁 Übergeordneter Ordner")
                    elif file_path.exists():
                        if file_path.is_file():
                            stat = file_path.stat()
                            size = self._format_file_size(stat.st_size)
                            modified = time.strftime("%d.%m.%Y %H:%M", time.localtime(stat.st_mtime))
                            info = f"📄 {file_path.name}\n💾 Größe: {size}\n📅 Geändert: {modified}"
                            self.file_info_text.insert(1.0, info)
                        else:
                            self.file_info_text.insert(1.0, f"📁 {file_path.name}\n(Ordner)")
                    else:
                        self.file_info_text.insert(1.0, "❌ Datei nicht gefunden")
                        
        except Exception as e:
            print(f"❌ File-Select-Fehler: {e}")
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Formatiert Dateigröße"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def _add_message(self, sender: str, message: str):
        """Fügt Nachricht zum Chat hinzu (Thread-safe)"""
        if not self.gui_ready or not self.chat_display:
            print(f"[{sender}]: {message}")
            return
        
        try:
            def add_to_gui():
                timestamp = time.strftime("%H:%M:%S")
                formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
                
                self.chat_display.insert(tk.END, formatted_message)
                self.chat_display.see(tk.END)
            
            if threading.current_thread() == threading.main_thread():
                add_to_gui()
            else:
                self.root.after(0, add_to_gui)
                
        except Exception as e:
            print(f"❌ Message-Add-Fehler: {e}")
    
    def _update_status(self, status: str):
        """Aktualisiert Status (Thread-safe)"""
        if not self.gui_ready or not self.status_label:
            return
        
        try:
            def update_gui():
                self.status_label.config(text=status)
            
            if threading.current_thread() == threading.main_thread():
                update_gui()
            else:
                self.root.after(0, update_gui)
                
        except Exception as e:
            print(f"❌ Status-Update-Fehler: {e}")
    
    def _on_send_message(self):
        """Sendet Nachricht"""
        if not self.gui_ready or not self.input_field:
            return
        
        try:
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
            
        except Exception as e:
            print(f"❌ Send-Message-Fehler: {e}")
    
    def _process_message(self, message: str):
        """Verarbeitet Nachricht (Thread-safe)"""
        try:
            self._update_status("🤔 Denke nach...")
            
            # System-Kommandos erkennen
            from ..gui.main_window import ToobixGUI
            temp_gui = ToobixGUI(self.ai_handler, self.speech_engine, self.desktop, self.settings)
            system_response = temp_gui._handle_system_commands(message)
            
            if system_response:
                self._add_message("Toobix", system_response)
                # TTS mit Error-Handling
                try:
                    if system_response and hasattr(self.speech_engine, 'speak'):
                        self.speech_engine.speak(system_response, wait=False)
                except:
                    pass  # TTS-Fehler ignorieren
                self._update_status("Bereit")
                return
            
            # KI-Antwort
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                self.ai_handler.get_response(message)
            )
            
            self._add_message("Toobix", response)
            
            # TTS mit Error-Handling
            try:
                if response and hasattr(self.speech_engine, 'speak'):
                    self.speech_engine.speak(response, wait=False)
            except:
                pass  # TTS-Fehler ignorieren
            
        except Exception as e:
            error_msg = f"❌ Entschuldigung, es gab einen Fehler: {e}"
            self._add_message("Toobix", error_msg)
        
        finally:
            self._update_status("Bereit")
    
    def _on_voice_input(self):
        """Voice-Input"""
        try:
            self._add_message("System", "🎤 Voice-Input wird in der optimierten Version bald verfügbar!")
        except Exception as e:
            print(f"❌ Voice-Input-Fehler: {e}")
    
    def _on_closing(self):
        """Beim Schließen der GUI"""
        try:
            self.is_running = False
            self.gui_ready = False
            
            if self.root:
                self.root.quit()
                self.root.destroy()
                
        except Exception as e:
            print(f"❌ Closing-Fehler: {e}")
    
    def run(self):
        """Startet die GUI (Thread-safe)"""
        if not self.root:
            print("❌ GUI konnte nicht erstellt werden")
            return
        
        try:
            print("🎨 Optimierte GUI gestartet")
            self.is_running = True
            self.root.mainloop()
        except Exception as e:
            print(f"❌ GUI-Run-Fehler: {e}")
        finally:
            self.is_running = False
    
    def close(self):
        """Schließt die GUI"""
        self._on_closing()
