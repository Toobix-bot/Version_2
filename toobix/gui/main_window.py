"""
Toobix GUI - Main Window
Moderne GUI mit Chat-Interface und Sprachsteuerung
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import asyncio
import time
import os
from pathlib import Path
from datetime import datetime
import psutil
from typing import Optional

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

class ToobixGUI:
    """Hauptfenster für Toobix AI Assistant"""
    
    def __init__(self, ai_handler, speech_engine, desktop, settings):
        self.ai_handler = ai_handler
        self.speech_engine = speech_engine
        self.desktop = desktop
        self.settings = settings
        
        self.gui_config = settings.get_gui_config()
        self.root = None
        self.chat_display = None
        self.input_field = None
        self.listening_status = None
        
        # Chat-Historie
        self.chat_history = []
        
        print("🎨 GUI wird initialisiert...")
        self._setup_gui()
        self._setup_callbacks()
    
    def _setup_gui(self):
        """Erstellt die GUI-Komponenten"""
        # Hauptfenster
        if CTK_AVAILABLE:
            ctk.set_appearance_mode(self.gui_config['theme'])
            self.root = ctk.CTk()
        else:
            self.root = tk.Tk()
        
        self.root.title("Toobix AI Assistant")
        self.root.geometry(f"{self.gui_config['width']}x{self.gui_config['height']}")
        
        # Nicht minimieren können
        self.root.resizable(True, True)
        
        # Icon setzen (falls vorhanden)
        try:
            self.root.iconbitmap("toobix_icon.ico")
        except:
            pass
        
        self._create_widgets()
        self._setup_bindings()
    
    def _create_widgets(self):
        """Erstellt alle GUI-Widgets"""
        
        # === HEADER ===
        header_frame = self._create_frame(self.root, height=60)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        # Toobix Logo/Titel
        title_label = self._create_label(
            header_frame, 
            "🤖 Toobix AI Assistant", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Status-Info
        self.listening_status = self._create_label(
            header_frame,
            "🎤 Bereit",
            font=("Arial", 10)
        )
        self.listening_status.pack(side="right", padx=10)
        
        # === CHAT BEREICH ===
        chat_frame = self._create_frame(self.root)
        chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Chat-Display
        if CTK_AVAILABLE:
            self.chat_display = ctk.CTkTextbox(
                chat_frame,
                height=400,
                font=("Arial", 11)
            )
        else:
            self.chat_display = scrolledtext.ScrolledText(
                chat_frame,
                height=20,
                font=("Arial", 11),
                wrap=tk.WORD
            )
        
        self.chat_display.pack(fill="both", expand=True, pady=(0, 10))
        
        # Willkommensnachricht
        self._add_message("Toobix", "Hallo! Ich bin Toobix, dein AI-Assistent. Du kannst mit mir sprechen oder hier tippen. 🚀")
        
        # === INPUT BEREICH ===
        input_frame = self._create_frame(self.root, height=80)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Eingabefeld
        if CTK_AVAILABLE:
            self.input_field = ctk.CTkEntry(
                input_frame,
                placeholder_text="Schreibe deine Nachricht hier oder drücke F1 für Spracheingabe...",
                font=("Arial", 12)
            )
        else:
            self.input_field = tk.Entry(
                input_frame,
                font=("Arial", 12)
            )
        
        self.input_field.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Buttons
        button_frame = self._create_frame(input_frame, width=200)
        button_frame.pack(side="right", fill="y")
        
        # Send Button
        self.send_button = self._create_button(
            button_frame,
            "Senden",
            self._on_send_message
        )
        self.send_button.pack(side="top", fill="x", pady=(0, 5))
        
        # Voice Button
        self.voice_button = self._create_button(
            button_frame,
            "🎤 Sprechen",
            self._on_voice_input
        )
        self.voice_button.pack(side="top", fill="x")
        
        # === BOTTOM STATUS ===
        status_frame = self._create_frame(self.root, height=30)
        status_frame.pack(fill="x", padx=10, pady=(0, 5))
        
        self.status_label = self._create_label(
            status_frame,
            f"Bereit - Ollama: {self.ai_handler.ollama_available}, Groq: {self.ai_handler.groq_available}",
            font=("Arial", 9)
        )
        self.status_label.pack(side="left")
        
        # AI Status Button
        self.ai_status_button = self._create_button(
            status_frame,
            "AI Status",
            self._show_ai_status,
            width=80
        )
        self.ai_status_button.pack(side="right")
    
    def _create_frame(self, parent, **kwargs):
        """Erstellt Frame-Widget je nach verfügbarer Bibliothek"""
        if CTK_AVAILABLE:
            return ctk.CTkFrame(parent, **kwargs)
        else:
            return ttk.Frame(parent, **kwargs)
    
    def _create_label(self, parent, text, **kwargs):
        """Erstellt Label-Widget"""
        if CTK_AVAILABLE:
            return ctk.CTkLabel(parent, text=text, **kwargs)
        else:
            return ttk.Label(parent, text=text, **kwargs)
    
    def _create_button(self, parent, text, command, **kwargs):
        """Erstellt Button-Widget"""
        if CTK_AVAILABLE:
            return ctk.CTkButton(parent, text=text, command=command, **kwargs)
        else:
            return ttk.Button(parent, text=text, command=command, **kwargs)
    
    def _setup_bindings(self):
        """Setzt Tastatur-Shortcuts und Events"""
        # Enter für Senden
        self.root.bind('<Return>', lambda e: self._on_send_message())
        
        # F1 für Spracheingabe
        self.root.bind('<F1>', lambda e: self._on_voice_input())
        
        # ESC für Fokus zurücksetzen
        self.root.bind('<Escape>', lambda e: self.input_field.focus())
        
        # Fenster schließen
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_callbacks(self):
        """Setzt Speech Engine Callbacks"""
        self.speech_engine.set_callbacks(
            on_command=self._on_speech_command,
            on_wake_word=self._on_wake_word
        )
    
    def _add_message(self, sender: str, message: str):
        """Fügt Nachricht zum Chat hinzu"""
        self.chat_history.append((sender, message))
        
        # Formatierung je nach Sender
        if sender == "Toobix":
            prefix = "🤖 "
            color = "blue" if not CTK_AVAILABLE else None
        else:
            prefix = "👤 "
            color = "green" if not CTK_AVAILABLE else None
        
        # Nachricht anzeigen
        if CTK_AVAILABLE:
            self.chat_display.insert("end", f"{prefix}{sender}: {message}\n\n")
        else:
            self.chat_display.insert("end", f"{prefix}{sender}: {message}\n\n")
            if color:
                # Farb-Tags für Tkinter (vereinfacht)
                pass
        
        # Auto-scroll
        self.chat_display.see("end")
    
    def _on_send_message(self):
        """Behandelt gesendete Text-Nachricht"""
        message = self.input_field.get().strip()
        if not message:
            return
        
        # Eingabefeld leeren
        self.input_field.delete(0, 'end')
        
        # Nachricht anzeigen
        self._add_message("Du", message)
        
        # AI-Antwort in separatem Thread
        threading.Thread(
            target=self._process_message,
            args=(message,),
            daemon=True
        ).start()
    
    def _on_voice_input(self):
        """Behandelt Spracheingabe-Button"""
        self.voice_button.configure(text="🎤 Höre...")
        self.voice_button.configure(state="disabled")
        
        # Sprache in separatem Thread
        threading.Thread(
            target=self._process_voice_input,
            daemon=True
        ).start()
    
    def _process_voice_input(self):
        """Verarbeitet Spracheingabe"""
        try:
            # Einmalige Spracherkennung
            text = self.speech_engine.manual_listen()
            
            if text:
                # UI aktualisieren (Thread-safe)
                self.root.after(0, lambda: self.input_field.insert(0, text))
                self.root.after(0, lambda: self._add_message("Du (Sprache)", text))
                
                # AI-Antwort verarbeiten
                self._process_message(text)
            
        finally:
            # Button zurücksetzen
            self.root.after(0, lambda: self.voice_button.configure(text="🎤 Sprechen"))
            self.root.after(0, lambda: self.voice_button.configure(state="normal"))
    
    def _process_message(self, message: str):
        """Verarbeitet Nachricht mit AI und logged Interaktionen"""
        try:
            # Lade-Status anzeigen
            self.root.after(0, lambda: self._update_status("🤔 Denke nach..."))
            
            # System-Kommandos erkennen und ausführen
            system_response = self._handle_system_commands(message)
            if system_response:
                # Logge System-Kommando in KnowledgeBase
                self.ai_handler.knowledge_base.log_interaction(message, system_response, {'type': 'system_command'})
                
                self.root.after(0, lambda: self._add_message("Toobix", system_response))
                if system_response:
                    self.speech_engine.speak(system_response, wait=False)
                self.root.after(0, lambda: self._update_status("Bereit"))
                return
            
            # Erstelle personalisierten Kontext für AI
            user_context = self.ai_handler.knowledge_base.create_user_context()
            
            # Async AI-Antwort holen mit Kontext
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Erweitere Prompt mit persönlichem Kontext
            enhanced_prompt = f"[Benutzer-Kontext: {user_context}]\n\nFrage: {message}"
            
            response = loop.run_until_complete(
                self.ai_handler.get_response(enhanced_prompt)
            )
            
            # Logge AI-Interaktion
            self.ai_handler.knowledge_base.log_interaction(message, response, {
                'type': 'ai_chat',
                'user_context': user_context,
                'model_used': self.ai_handler.get_status().get('current_model', 'unknown')
            })
            
            # Antwort anzeigen
            self.root.after(0, lambda: self._add_message("Toobix", response))
            
            # TTS wenn aktiviert
            if response:
                self.speech_engine.speak(response, wait=False)
            
        except Exception as e:
            error_msg = f"Entschuldigung, es gab einen Fehler: {e}"
            
            # Logge auch Fehler
            self.ai_handler.knowledge_base.log_interaction(message, error_msg, {'type': 'error'})
            
            self.root.after(0, lambda: self._add_message("Toobix", error_msg))
        
        finally:
            self.root.after(0, lambda: self._update_status("Bereit"))
    
    def _handle_system_commands(self, message: str) -> Optional[str]:
        """Behandelt direkte System-Kommandos inkl. neue Projekt- und Wissensfunktionen"""
        message_lower = message.lower()
        
        # === WISSENSBASIS BEFEHLE ===
        # Erinnerung speichern: "merke dir xyz als ..."
        if message_lower.startswith('merke dir ') or 'merke:' in message_lower:
            try:
                if 'als ' in message_lower:
                    parts = message_lower.split(' als ')
                    if len(parts) >= 2:
                        key = parts[0].replace('merke dir ', '').strip()
                        value_note = parts[1].strip()
                        if ' - ' in value_note:
                            value, note = value_note.split(' - ', 1)
                        else:
                            value, note = value_note, None
                        category = 'allgemein'
                        return self.ai_handler.knowledge_base.remember_fact(category, key, value, note)
                
                # Fallback: Merke als Notiz
                content = message_lower.replace('merke dir ', '').replace('merke:', '').strip()
                return self.ai_handler.knowledge_base.remember_fact('notizen', f"notiz_{int(time.time())}", content)
            except Exception as e:
                return f"❌ Fehler beim Speichern: {e}"
        
        # Erinnerung abrufen: "was weißt du über..."
        if any(phrase in message_lower for phrase in ['was weißt du über', 'erinnerst du dich an', 'was hast du über']):
            try:
                query = message_lower
                for phrase in ['was weißt du über ', 'erinnerst du dich an ', 'was hast du über ']:
                    query = query.replace(phrase, '')
                query = query.strip(' ?')
                return self.ai_handler.knowledge_base.recall_fact('allgemein', query)
            except:
                return self.ai_handler.knowledge_base.get_memory_summary()
        
        # Wissens-Zusammenfassung
        if any(phrase in message_lower for phrase in ['zeige erinnerungen', 'was weißt du', 'memory summary']):
            return self.ai_handler.knowledge_base.get_memory_summary()
        
        # Personalisierte Vorschläge
        if any(phrase in message_lower for phrase in ['vorschläge', 'empfehlungen', 'was soll ich']):
            suggestions = self.ai_handler.knowledge_base.get_personalized_suggestions()
            if suggestions:
                return "💡 PERSONALISIERTE VORSCHLÄGE:\n\n" + "\n".join(suggestions)
            else:
                return "🤖 Ich lerne noch deine Gewohnheiten kennen. Nutze mich einfach weiter!"
        
        # === PROJEKT-ANALYSE BEFEHLE ===
        # Projekte scannen
        if any(phrase in message_lower for phrase in ['scanne projekte', 'finde projekte', 'projekt scan']):
            try:
                # Standard-Verzeichnisse oder aktuelles
                scan_dirs = ['C:\\Users\\' + os.getenv('USERNAME') + '\\Documents', 
                           'C:\\Users\\' + os.getenv('USERNAME') + '\\Desktop']
                projects = self.ai_handler.project_analyzer.scan_for_projects(scan_dirs)
                
                if not projects:
                    return "🔍 Keine Projekte in den Standard-Verzeichnissen gefunden."
                
                result = f"🔍 {len(projects)} PROJEKTE GEFUNDEN:\n\n"
                for project in projects[:10]:  # Erste 10
                    result += f"📁 {project['name']}\n"
                    result += f"   📍 {project['path']}\n" 
                    result += f"   🔧 {project['language']} | Score: {project['score']}\n"
                    result += f"   📄 {project['file_count']} Dateien\n\n"
                
                if len(projects) > 10:
                    result += f"... und {len(projects) - 10} weitere Projekte"
                
                return result
            except Exception as e:
                return f"❌ Fehler beim Projekt-Scan: {e}"
        
        # Projekt-Organisation
        if any(phrase in message_lower for phrase in ['organisiere projekte', 'projekt organisation', 'ordne projekte']):
            try:
                scan_dirs = ['C:\\Users\\' + os.getenv('USERNAME') + '\\Documents']
                plan = self.ai_handler.project_analyzer.create_project_organization_plan(scan_dirs)
                return plan
            except Exception as e:
                return f"❌ Fehler bei Projekt-Organisation: {e}"
        
        # Duplikate finden
        if any(phrase in message_lower for phrase in ['finde duplikate', 'doppelte projekte', 'duplicates']):
            try:
                scan_dirs = ['C:\\Users\\' + os.getenv('USERNAME') + '\\Documents']
                projects = self.ai_handler.project_analyzer.scan_for_projects(scan_dirs)
                duplicates = self.ai_handler.project_analyzer._find_duplicate_projects(projects)
                
                if not duplicates:
                    return "✅ Keine doppelten Projekte gefunden!"
                
                result = f"⚠️ {len(duplicates)} DUPLIKAT-GRUPPEN GEFUNDEN:\n\n"
                for i, dup_group in enumerate(duplicates, 1):
                    result += f"Gruppe {i}:\n"
                    for proj in dup_group:
                        result += f"  📁 {proj['name']} - {proj['path']}\n"
                    result += "\n"
                
                return result
            except Exception as e:
                return f"❌ Fehler bei Duplikat-Suche: {e}"
        
        # === ERWEITERTE ORGANISATIONS-BEFEHLE ===
        # Komplette System-Organisation
        if any(phrase in message_lower for phrase in ['komplette system organisation', 'system organisation', 'organisiere alles', 'master organisation']):
            try:
                result = self.ai_handler.advanced_organizer.execute_comprehensive_organization()
                if result['overall_success']:
                    response = "🎯 KOMPLETTE SYSTEM-ORGANISATION DURCHGEFÜHRT!\n\n"
                    response += f"⏱️ Dauer: {result['total_time']:.1f} Sekunden\n\n"
                    
                    for phase_name, phase_result in result['phases'].items():
                        if phase_result.get('success', False):
                            response += f"✅ {phase_name.upper()}: Erfolgreich\n"
                        else:
                            response += f"❌ {phase_name.upper()}: Fehler\n"
                    
                    response += "\n🏗️ Master-Struktur erstellt in TOOBIX_ORGANISATION/"
                    response += "\n📊 System-Analyse abgeschlossen"
                    response += "\n🧹 Aufräumung durchgeführt"
                    response += "\n⚙️ Automation konfiguriert"
                else:
                    response = f"❌ System-Organisation fehlgeschlagen: {result.get('error', 'Unbekannter Fehler')}"
                return response
            except Exception as e:
                return f"❌ Fehler bei System-Organisation: {e}"
        
        # Master-Struktur erstellen
        if any(phrase in message_lower for phrase in ['erstelle ordnerstruktur', 'erstelle master struktur', 'master struktur']):
            try:
                result = self.ai_handler.advanced_organizer.create_master_structure()
                if result['success']:
                    return f"🏗️ MASTER-STRUKTUR ERSTELLT!\n\n📁 Basis-Pfad: {result['base_path']}\n✅ {result['folder_count']} Ordner erstellt\n\n🔍 Schau in TOOBIX_ORGANISATION/ für die neue Struktur!"
                else:
                    return f"❌ Struktur-Erstellung fehlgeschlagen: {result['error']}"
            except Exception as e:
                return f"❌ Fehler bei Struktur-Erstellung: {e}"
        
        # System-Analyse erweitert
        if any(phrase in message_lower for phrase in ['analyse system umfassend', 'system vollanalyse', 'comprehensive analysis']):
            try:
                analysis = self.ai_handler.advanced_organizer.analyze_system_comprehensive()
                
                response = "🔍 UMFASSENDE SYSTEM-ANALYSE:\n\n"
                
                # System-Gesundheit
                health = analysis.get('system_health', {})
                if 'error' not in health:
                    status_emoji = "🟢" if health['status'] == 'excellent' else "🟡" if health['status'] in ['good', 'warning'] else "🔴"
                    response += f"{status_emoji} System-Gesundheit: {health['status'].upper()} ({health['score']}/100)\n"
                    response += f"💾 RAM: {health['memory_percent']:.1f}% | Disk: {health['disk_percent']:.1f}% | CPU: {health['cpu_percent']:.1f}%\n"
                    response += f"📊 Freier Speicher: {health['free_space_gb']:.1f} GB\n\n"
                
                # Aufräum-Möglichkeiten
                cleanup = analysis.get('cleanup_opportunities', [])
                if cleanup and len(cleanup) > 0:
                    response += "🧹 AUFRÄUM-MÖGLICHKEITEN:\n"
                    for opp in cleanup[:5]:  # Top 5
                        safety = "🛡️" if opp['safety'] == 'safe' else "⚠️"
                        response += f"{safety} {opp['description']} → {opp['estimated_savings_mb']:.1f} MB\n"
                    response += "\n"
                
                # Organisations-Vorschläge
                suggestions = analysis.get('organization_suggestions', [])
                if suggestions:
                    response += "💡 ORGANISATIONS-VORSCHLÄGE:\n"
                    for sug in suggestions[:3]:  # Top 3
                        impact = "🔥" if sug['impact'] == 'high' else "⚡" if sug['impact'] == 'medium' else "💫"
                        response += f"{impact} {sug['title']} (Impact: {sug['impact']})\n"
                
                return response
            except Exception as e:
                return f"❌ Fehler bei umfassender Analyse: {e}"
        
        # ECHTE Speicherfresser finden
        if any(phrase in message_lower for phrase in ['finde speicherfresser', 'was frisst ram', 'ram verbraucher', 'memory hogs', 'was frisst meinen ram']):
            try:
                ram_data = self.ai_handler.real_system_manager.get_real_ram_usage()
                
                if 'error' in ram_data:
                    return f"❌ {ram_data['error']}"
                
                response = f"🔍 ECHTE RAM-VERBRAUCHER:\n\n"
                response += f"💾 RAM-Status: {ram_data['used_gb']:.1f}/{ram_data['total_gb']:.1f} GB ({ram_data['percent']:.1f}%)\n"
                response += f"🟢 Verfügbar: {ram_data['available_gb']:.1f} GB\n\n"
                
                response += "🥇 TOP RAM-FRESSER:\n"
                for i, proc in enumerate(ram_data['top_processes'][:8], 1):
                    response += f"{i:2}. {proc['name']:<20} → {proc['memory_mb']:.0f} MB ({proc['memory_percent']:.1f}%)\n"
                
                response += f"\n💡 Verwende 'beende [programmname]' zum Schließen!"
                return response
                
            except Exception as e:
                return f"❌ Fehler bei RAM-Analyse: {e}"
                
                return response
            except Exception as e:
                return f"❌ Fehler bei Speicherfresser-Analyse: {e}"
        
        # ECHTE Programme beenden
        if any(phrase in message_lower for phrase in ['beende', 'schließe', 'kill', 'stop']):
            try:
                # Programmnamen extrahieren
                words = message_lower.split()
                if len(words) >= 2:
                    program_name = words[1]
                    
                    # Bekannte Programm-Aliases
                    aliases = {
                        'chrome': 'chrome.exe',
                        'firefox': 'firefox.exe', 
                        'edge': 'msedge.exe',
                        'outlook': 'outlook.exe',
                        'teams': 'Teams.exe',
                        'skype': 'Skype.exe',
                        'discord': 'Discord.exe',
                        'steam': 'steam.exe',
                        'notepad': 'notepad.exe',
                        'excel': 'excel.exe',
                        'word': 'winword.exe',
                        'photoshop': 'Photoshop.exe'
                    }
                    
                    # Programm-Name normalisieren
                    if program_name in aliases:
                        program_name = aliases[program_name]
                    elif not program_name.endswith('.exe'):
                        program_name += '.exe'
                    
                    # Echtes Beenden
                    result = self.ai_handler.real_system_manager.kill_process_real(program_name)
                    
                    if result['success']:
                        if result['killed_count'] > 0:
                            response = f"✅ {result['killed_count']} Instanz(en) von {program_name} beendet!"
                            if result['errors']:
                                response += f"\n⚠️ {len(result['errors'])} Fehler aufgetreten"
                        else:
                            response = f"ℹ️ {program_name} war nicht aktiv"
                    else:
                        response = f"❌ Fehler: {result['error']}"
                    
                    return response
                else:
                    return "❌ Bitte gib ein Programm an: 'beende chrome'"
                    
            except Exception as e:
                return f"❌ Fehler beim Beenden: {e}"
        
        # ECHTE Datei-Organisation
        if any(phrase in message_lower for phrase in ['organisiere dateien', 'sortiere dateien', 'aufräumen downloads', 'organisiere desktop']):
            try:
                from pathlib import Path
                
                # Quell-Ordner bestimmen
                if 'downloads' in message_lower:
                    source_dir = str(Path.home() / 'Downloads')
                elif 'desktop' in message_lower:
                    source_dir = str(Path.home() / 'Desktop')  
                elif 'dokumente' in message_lower:
                    source_dir = str(Path.home() / 'Documents')
                else:
                    source_dir = str(Path.home() / 'Downloads')  # Standard
                
                result = self.ai_handler.real_system_manager.organize_files_real(source_dir)
                
                if result['success']:
                    response = f"✅ DATEI-ORGANISATION ERFOLGREICH!\n\n"
                    response += f"📁 Quell-Ordner: {source_dir}\n"
                    response += f"🏗️ Ziel-Ordner: {result['organization_path']}\n"
                    response += f"📄 Dateien verschoben: {result['moved_files']}\n"
                    
                    if result['errors'] > 0:
                        response += f"⚠️ Fehler: {result['errors']}\n"
                    
                    # Details der ersten 5 verschobenen Dateien
                    if result['details']:
                        response += f"\n📋 BEISPIELE:\n"
                        for detail in result['details'][:5]:
                            filename = Path(detail['target']).name
                            category = detail['category'].upper()
                            response += f"• {filename} → {category}\n"
                        
                        if len(result['details']) > 5:
                            response += f"... und {len(result['details']) - 5} weitere\n"
                else:
                    response = f"❌ Organisation fehlgeschlagen: {result['error']}"
                
                return response
                
        # ERWEITERTE SYSTEM-ÜBERWACHUNG
        if any(phrase in message_lower for phrase in ['erweiterte überwachung', 'system monitoring', 'performance dashboard', 'system health']):
            try:
                # Starte erweiterte Überwachung
                if not self.ai_handler.advanced_monitor.monitoring_active:
                    self.ai_handler.advanced_monitor.start_monitoring()
                
                # Performance-Report erstellen
                report = self.ai_handler.advanced_monitor.get_performance_report()
                
                if 'error' in report:
                    return f"❌ Fehler beim Performance-Report: {report['error']}"
                
                health = report['health_score']
                current = report['current_metrics']
                trends = report['trends']
                
                response = f"📊 ERWEITERTE SYSTEM-ANALYSE:\n\n"
                response += f"🏥 System-Gesundheit: {health['status']} ({health['score']}/100)\n"
                response += f"   • CPU-Score: {health['details']['cpu_score']}/100\n"
                response += f"   • Memory-Score: {health['details']['memory_score']}/100\n"
                response += f"   • Disk-Score: {health['details']['disk_score']}/100\n\n"
                
                response += f"📈 PERFORMANCE-TRENDS:\n"
                response += f"   • CPU-Durchschnitt: {trends['cpu_average']}%\n"
                response += f"   • Memory-Durchschnitt: {trends['memory_average']}%\n\n"
                
                response += f"🚀 AUTOSTART-PROGRAMME: {report['startup_programs']['count']}\n"
                response += f"🌐 NETZWERK-VERBINDUNGEN: {report['network']['active_connections']}\n\n"
                
                if report['recommendations']:
                    response += f"💡 EMPFEHLUNGEN:\n"
                    for rec in report['recommendations'][:3]:
                        response += f"   • {rec}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Fehler bei erweiterter System-Überwachung: {e}"
        
        # GIT-INTEGRATION
        if any(phrase in message_lower for phrase in ['git scan', 'git repositories', 'git dashboard', 'repo übersicht']):
            try:
                dashboard = self.ai_handler.git_integration.get_repository_dashboard()
                
                summary = dashboard['summary']
                response = f"🔧 GIT-REPOSITORY DASHBOARD:\n\n"
                response += f"📊 ÜBERSICHT:\n"
                response += f"   • Repositories gesamt: {summary['total_repositories']}\n"
                response += f"   • Gesunde Repos: {summary['healthy_repositories']}\n"
                response += f"   • Mit Änderungen: {summary['repositories_with_changes']}\n"
                response += f"   • Hinter Remote: {summary['repositories_behind']}\n"
                response += f"   • Gesundheit: {summary['health_percentage']}%\n\n"
                
                if dashboard['top_languages']:
                    response += f"💻 TOP PROGRAMMIERSPRACHEN:\n"
                    for lang in dashboard['top_languages'][:3]:
                        response += f"   • {lang['language']}: {lang['lines']:,} Zeilen in {lang['repositories']} Repos\n"
                    response += "\n"
                
                if dashboard['problem_repositories']:
                    response += f"⚠️ PROBLEMATISCHE REPOSITORIES:\n"
                    for repo in dashboard['problem_repositories'][:3]:
                        response += f"   • {repo['name']} (Score: {repo['health_score']}/100)\n"
                        for issue in repo['issues'][:2]:
                            response += f"     - {issue}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Fehler bei Git-Dashboard: {e}"
        
        # GIT-OPERATIONEN
        if any(phrase in message_lower for phrase in ['git pull all', 'git push all', 'git commit all', 'bulk git']):
            try:
                operation = 'status'
                if 'pull' in message_lower:
                    operation = 'pull'
                elif 'push' in message_lower:
                    operation = 'push'
                elif 'commit' in message_lower:
                    operation = 'commit'
                
                result = self.ai_handler.git_integration.bulk_git_operations(operation)
                
                response = f"🔧 BULK GIT-{operation.upper()}:\n\n"
                response += f"📊 ERGEBNIS:\n"
                response += f"   • Gesamt: {result['total']}\n"
                response += f"   • Erfolgreich: {len(result['successful'])}\n"
                response += f"   • Fehlgeschlagen: {len(result['failed'])}\n"
                response += f"   • Übersprungen: {len(result['skipped'])}\n\n"
                
                if result['successful']:
                    response += f"✅ ERFOLGREICH:\n"
                    for repo in result['successful'][:3]:
                        response += f"   • {repo['name']}: {repo.get('message', 'OK')}\n"
                
                if result['failed']:
                    response += f"\n❌ FEHLGESCHLAGEN:\n"
                    for repo in result['failed'][:3]:
                        response += f"   • {repo['name']}: {repo['error']}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Fehler bei Git-Operation: {e}"
        
        # AUTOMATION RULES
        if any(phrase in message_lower for phrase in ['create rule', 'automation', 'task rule', 'erstelle regel']):
            try:
                if 'backup' in message_lower and 'daily' in message_lower:
                    # Beispiel: Tägliches Backup
                    rule_data = {
                        'name': 'Daily Desktop Backup',
                        'description': 'Tägliches Backup wichtiger Desktop-Dateien',
                        'triggers': [{
                            'type': 'time',
                            'config': {
                                'hour': 20,
                                'minute': 0,
                                'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
                            }
                        }],
                        'actions': [{
                            'type': 'backup_files',
                            'config': {
                                'source_directory': str(Path.home() / 'Desktop'),
                                'backup_location': str(Path.home() / 'ToobixBackups' / 'Desktop')
                            }
                        }]
                    }
                    
                    result = self.ai_handler.task_scheduler.create_automation_rule(rule_data)
                    if result['success']:
                        return f"✅ Automatisierungs-Regel erstellt: {rule_data['name']}\n📅 Backup läuft täglich um 20:00 Uhr"
                    else:
                        return f"❌ Fehler beim Erstellen der Regel: {result.get('error', 'Unbekannter Fehler')}"
                
                return "🤖 AUTOMATION VERFÜGBAR:\n• 'create daily backup rule' - Tägliches Backup\n• 'show automation rules' - Regel-Übersicht\n• 'automation dashboard' - Status-Dashboard"
                
            except Exception as e:
                return f"❌ Fehler bei Automation: {e}"
        
        # AUTOMATION DASHBOARD
        if any(phrase in message_lower for phrase in ['automation dashboard', 'show rules', 'regel übersicht']):
            try:
                dashboard = self.ai_handler.task_scheduler.get_automation_dashboard()
                
                response = f"🤖 AUTOMATION DASHBOARD:\n\n"
                response += f"📊 ÜBERSICHT:\n"
                response += f"   • Aktive Regeln: {dashboard['active_rules']}\n"
                response += f"   • Inaktive Regeln: {dashboard['inactive_rules']}\n"
                response += f"   • Heute ausgeführt: {dashboard['executions_today']}\n"
                response += f"   • Letzte Stunde: {dashboard['executions_last_hour']}\n\n"
                
                if dashboard['recent_executions']:
                    response += f"🕒 LETZTE AUSFÜHRUNGEN:\n"
                    for exec in dashboard['recent_executions'][:3]:
                        status_icon = "✅" if exec['success'] else "❌"
                        response += f"   {status_icon} {exec['rule_name']} - {exec['timestamp']}\n"
                
                if dashboard['upcoming_executions']:
                    response += f"\n⏰ NÄCHSTE AUSFÜHRUNGEN:\n"
                    for upcoming in dashboard['upcoming_executions'][:3]:
                        response += f"   📅 {upcoming['rule_name']} - {upcoming['next_execution']}\n"
                
                return response
                
            except Exception as e:
                return f"❌ Fehler bei Automation-Dashboard: {e}"
        
        # PHASE 3: KI-ENHANCED FEATURES
        
        # CONTEXT ANALYTICS
        if any(phrase in message_lower for phrase in ['context analytics', 'working context', 'kontext analyse']):
            try:
                if hasattr(self.ai_handler, 'context_manager') and self.ai_handler.context_manager:
                    analytics = self.ai_handler.context_manager.get_context_analytics()
                    
                    response = f"🧠 KONTEXT-ANALYTICS:\n\n"
                    response += f"📊 AKTUELLER STATUS:\n"
                    response += f"   • Kontext: {analytics['current_context']}\n"
                    response += f"   • Session-Dauer: {analytics['session_duration']} min\n"
                    response += f"   • Energy Level: {analytics['energy_level']:.0f}%\n\n"
                    
                    if analytics['stress_indicators']:
                        response += f"⚠️ STRESS-INDIKATOREN:\n"
                        for indicator in analytics['stress_indicators']:
                            response += f"   • {indicator}\n"
                        response += "\n"
                    
                    if analytics['recommendations']:
                        response += f"💡 EMPFEHLUNGEN:\n"
                        for rec in analytics['recommendations'][:3]:
                            response += f"   • {rec}\n"
                    
                    return response
                else:
                    return "❌ Context Manager nicht verfügbar"
                    
            except Exception as e:
                return f"❌ Fehler bei Context Analytics: {e}"
        
        # PRODUCTIVITY GAMIFICATION
        if any(phrase in message_lower for phrase in ['gamification', 'level up', 'achievements', 'xp dashboard']):
            try:
                if hasattr(self.ai_handler, 'gamification') and self.ai_handler.gamification:
                    dashboard = self.ai_handler.gamification.get_productivity_dashboard()
                    
                    response = f"🎮 PRODUCTIVITY GAMIFICATION:\n\n"
                    response += f"👤 DEIN PROFIL:\n"
                    response += f"   • Level: {dashboard['user_stats']['level']}\n"
                    response += f"   • XP: {dashboard['user_stats']['total_xp']:,}\n"
                    response += f"   • Streak: {dashboard['streak_info']['current_streak']} Tage\n"
                    response += f"   • Aufgaben: {dashboard['user_stats']['tasks_completed']}\n\n"
                    
                    # Level Progress
                    progress = dashboard['level_progress']['progress_percentage']
                    response += f"📈 LEVEL PROGRESS: {progress:.0f}%\n"
                    progress_bar = "█" * int(progress/10) + "░" * (10 - int(progress/10))
                    response += f"   [{progress_bar}]\n\n"
                    
                    # Daily Challenges
                    if dashboard['daily_challenges']:
                        response += f"🎯 DAILY CHALLENGES:\n"
                        for challenge in dashboard['daily_challenges'][:2]:
                            progress_pct = (challenge['current_progress'] / challenge['target_value']) * 100
                            response += f"   • {challenge['name']}: {progress_pct:.0f}%\n"
                        response += "\n"
                    
                    # Recent Achievements
                    if dashboard['recent_achievements']:
                        response += f"🏆 RECENT ACHIEVEMENTS:\n"
                        for ach in dashboard['recent_achievements'][:2]:
                            response += f"   • {ach['icon']} {ach['name']}\n"
                    
                    response += f"\n{dashboard['motivational_message']}"
                    
                    return response
                else:
                    return "❌ Gamification nicht verfügbar"
                    
            except Exception as e:
                return f"❌ Fehler bei Gamification: {e}"
        
        # DEEP ANALYTICS
        if any(phrase in message_lower for phrase in ['deep analytics', 'productivity patterns', 'analytics dashboard']):
            try:
                if hasattr(self.ai_handler, 'analytics_engine') and self.ai_handler.analytics_engine:
                    dashboard = self.ai_handler.analytics_engine.get_analytics_dashboard()
                    
                    response = f"🔬 DEEP ANALYTICS:\n\n"
                    response += f"📊 OVERVIEW:\n"
                    response += f"   • Datenpunkte: {dashboard['overview']['data_points']}\n"
                    response += f"   • Patterns erkannt: {dashboard['overview']['patterns_identified']}\n"
                    response += f"   • Analyse-Confidence: {dashboard['overview']['analysis_confidence']:.0%}\n\n"
                    
                    # Performance Trends
                    if 'performance_trends' in dashboard and dashboard['performance_trends']:
                        trends = dashboard['performance_trends']
                        if 'performance_change' in trends:
                            change = trends['performance_change']
                            trend_icon = "📈" if change > 0 else "📉"
                            response += f"{trend_icon} PERFORMANCE TREND: {change:+.1f}%\n"
                            response += f"   Status: {trends['trend_direction']}\n\n"
                    
                    # Optimization Opportunities
                    if dashboard.get('optimization_opportunities'):
                        response += f"🎯 OPTIMIERUNGSMÖGLICHKEITEN:\n"
                        for opp in dashboard['optimization_opportunities'][:2]:
                            response += f"   • {opp['title']}: {opp['description']}\n"
                        response += "\n"
                    
                    # Smart Recommendations
                    if dashboard.get('recommendations'):
                        response += f"💡 KI-EMPFEHLUNGEN:\n"
                        for rec in dashboard['recommendations'][:3]:
                            response += f"   • {rec}\n"
                    
                    return response
                else:
                    return "❌ Analytics Engine nicht verfügbar"
                    
            except Exception as e:
                return f"❌ Fehler bei Deep Analytics: {e}"
        
        # WELLNESS ENGINE
        if any(phrase in message_lower for phrase in ['wellness', 'meditation', 'soundscape', 'breathing']):
            try:
                if hasattr(self.ai_handler, 'wellness_engine') and self.ai_handler.wellness_engine:
                    
                    # Spezifische Wellness-Aktionen
                    if 'start meditation' in message_lower:
                        duration = 10  # Default
                        if '5 min' in message_lower:
                            duration = 5
                        elif '15 min' in message_lower:
                            duration = 15
                        
                        result = self.ai_handler.wellness_engine.start_meditation_session('mindfulness', duration)
                        if result['success']:
                            return f"🧘 Meditation gestartet!\n\nTyp: {result['type']}\nDauer: {result['duration']} Minuten\nSoundscape: {result['soundscape']}\n\nAnleitung:\n" + "\n".join(f"• {step}" for step in result['guidance'][:3])
                        else:
                            return f"❌ Meditation konnte nicht gestartet werden"
                    
                    elif 'start breathing' in message_lower or 'atemübung' in message_lower:
                        pattern = '4-7-8'  # Default
                        if 'box' in message_lower:
                            pattern = 'box'
                        elif 'energizing' in message_lower:
                            pattern = 'energizing'
                        
                        result = self.ai_handler.wellness_engine.start_breathing_exercise(pattern)
                        if result['success']:
                            return f"🫁 Atemübung gestartet!\n\nPattern: {result['pattern']}\nBeschreibung: {result['config']['description']}\nDauer: {result['config']['duration']} Minuten\n\nAnleitung:\n" + "\n".join(f"• {step}" for step in result['instructions'][:4])
                        else:
                            return f"❌ Atemübung konnte nicht gestartet werden"
                    
                    elif 'soundscape' in message_lower or 'focus sounds' in message_lower:
                        profile = 'Deep Focus'  # Default
                        if 'creative' in message_lower:
                            profile = 'Creative Flow'
                        elif 'relax' in message_lower or 'zen' in message_lower:
                            profile = 'Zen Garden'
                        elif 'energy' in message_lower:
                            profile = 'Energizer'
                        elif 'nature' in message_lower:
                            profile = 'Nature Immersion'
                        
                        result = self.ai_handler.wellness_engine.start_soundscape(profile)
                        if result['success']:
                            return f"🎵 Soundscape aktiviert!\n\nProfil: {result['profile']['name']}\nBeschreibung: {result['profile']['description']}\nMood: {result['profile']['mood']}\nIntensität: {result['profile']['intensity']}"
                        else:
                            return f"❌ Soundscape konnte nicht gestartet werden: {result.get('error', 'Unbekannter Fehler')}"
                    
                    else:
                        # Wellness Dashboard
                        dashboard = self.ai_handler.wellness_engine.get_wellness_dashboard()
                        
                        response = f"🎵 WELLNESS DASHBOARD:\n\n"
                        response += f"🌟 AKTUELLER STATUS:\n"
                        response += f"   • Stress Level: {dashboard['current_state']['stress_level']:.0f}%\n"
                        response += f"   • Energy Level: {dashboard['current_state']['energy_level']:.0f}%\n"
                        
                        if dashboard['current_state']['active_soundscape']:
                            response += f"   • Aktive Soundscape: {dashboard['current_state']['active_soundscape']}\n"
                        response += "\n"
                        
                        # Daily Summary
                        response += f"📊 HEUTE:\n"
                        response += f"   • Wellness-Sessions: {dashboard['daily_summary']['sessions_today']}\n"
                        response += f"   • Wellness-Zeit: {dashboard['daily_summary']['total_wellness_time']} min\n\n"
                        
                        # Quick Actions
                        response += f"⚡ QUICK ACTIONS:\n"
                        for action in dashboard['quick_actions'][:3]:
                            response += f"   {action['icon']} {action['name']}\n"
                        response += "\n"
                        
                        # Personalized Recommendations
                        if dashboard['personalized_recommendations']:
                            response += f"💡 EMPFEHLUNGEN:\n"
                            for rec in dashboard['personalized_recommendations']:
                                response += f"   • {rec}\n"
                        
                        return response
                else:
                    return "❌ Wellness Engine nicht verfügbar"
                    
            except Exception as e:
                return f"❌ Fehler bei Wellness Engine: {e}"
        
        # Große Dateien finden
        if any(phrase in message_lower for phrase in ['zeige große dateien', 'große dateien', 'big files', 'disk space']):
            try:
                from pathlib import Path
                import os
                
                large_files = []
                scan_dirs = [
                    Path.home() / 'Downloads',
                    Path.home() / 'Documents',
                    Path.home() / 'Desktop'
                ]
                
                for scan_dir in scan_dirs:
                    if scan_dir.exists():
                        for file_path in scan_dir.rglob('*'):
                            try:
                                if file_path.is_file():
                                    size = file_path.stat().st_size
                                    if size > 100 * 1024 * 1024:  # > 100MB
                                        large_files.append({
                                            'path': str(file_path),
                                            'name': file_path.name,
                                            'size_mb': size / (1024 * 1024),
                                            'size_gb': size / (1024 * 1024 * 1024)
                                        })
                            except (PermissionError, OSError):
                                continue
                
                large_files.sort(key=lambda x: x['size_mb'], reverse=True)
                
                if not large_files:
                    return "✅ Keine großen Dateien (>100MB) in Standard-Ordnern gefunden!"
                
                response = f"📊 {len(large_files)} GROSSE DATEIEN GEFUNDEN:\n\n"
                for i, file_info in enumerate(large_files[:10], 1):
                    if file_info['size_gb'] >= 1:
                        size_str = f"{file_info['size_gb']:.1f} GB"
                    else:
                        size_str = f"{file_info['size_mb']:.0f} MB"
                    response += f"{i:2}. {file_info['name']:<30} → {size_str}\n"
                    response += f"     📁 {os.path.dirname(file_info['path'])}\n\n"
                
                if len(large_files) > 10:
                    total_size_gb = sum(f['size_gb'] for f in large_files)
                    response += f"\n📊 Gesamt: {total_size_gb:.1f} GB in {len(large_files)} Dateien"
                
                return response
            except Exception as e:
                return f"❌ Fehler bei Dateigrößen-Analyse: {e}"
        
        # === BESTEHENDE SYSTEM-BEFEHLE ===
        # System-Analyse
        if any(word in message_lower for word in ['analysiere system', 'system analyse', 'system prüfen']):
            return self.desktop.analyze_system_cleanliness()
        
        # Aufräumplan erstellen
        if any(word in message_lower for word in ['aufräumplan', 'aufräumen plan', 'cleanup plan']):
            return self.desktop.create_cleanup_plan()
        
        # Backup erstellen
        if any(word in message_lower for word in ['backup erstellen', 'sicherung', 'backup']):
            return self.desktop.create_backup()
        
        # Aufräumung starten
        if any(word in message_lower for word in ['aufräumen starten', 'cleanup', 'aufräumen']):
            confirm = 'bestätigt' in message_lower or 'bestätige' in message_lower
            return self.desktop.execute_cleanup(confirm)
        
        # Programm öffnen
        if message_lower.startswith('öffne '):
            program = message_lower.replace('öffne ', '').strip()
            success = self.desktop.open_program(program)
            if success:
                return f"✅ {program} wurde geöffnet!"
            else:
                return f"❌ Konnte {program} nicht öffnen."
        
        # === SYSTEM-MONITORING BEFEHLE ===
        # System-Status anzeigen
        if any(phrase in message_lower for phrase in ['system status', 'zeige system status', 'realtime stats']):
            try:
                stats = self.ai_handler.system_monitor.get_real_time_stats()
                health = self.ai_handler.system_monitor.check_system_health()
                
                result = f"📊 SYSTEM-STATUS (ECHTZEIT):\n\n"
                result += f"🏥 Gesundheit: {health['status'].upper()}\n"
                result += f"{health['summary']}\n\n"
                
                result += f"🖥️ CPU: {stats['cpu']['usage_percent']}% ({stats['cpu']['cores']} Kerne)\n"
                result += f"💾 RAM: {stats['memory']['used_gb']}/{stats['memory']['total_gb']} GB ({stats['memory']['usage_percent']}%)\n"
                
                # Festplatten
                for device, disk_info in stats['disk'].items():
                    if device != 'io' and isinstance(disk_info, dict):
                        result += f"💽 {device}: {disk_info['usage_percent']}% ({disk_info['free_gb']} GB frei)\n"
                
                result += f"⏰ Uptime: {stats['uptime']['formatted']}\n"
                
                if health['alerts']:
                    result += f"\n⚠️ WARNUNGEN:\n"
                    for alert in health['alerts']:
                        result += f"• {alert}\n"
                
                return result
            except Exception as e:
                return f"❌ Fehler beim System-Status: {e}"
        
        # Detaillierter System-Bericht
        if any(phrase in message_lower for phrase in ['system bericht', 'system report', 'detaillierter system']):
            try:
                return self.ai_handler.system_monitor.generate_system_report()
            except Exception as e:
                return f"❌ Fehler beim System-Bericht: {e}"
        
        # System-Gesundheitscheck
        if any(phrase in message_lower for phrase in ['system health', 'system gesundheit', 'health check']):
            try:
                health = self.ai_handler.system_monitor.check_system_health()
                
                result = f"🏥 SYSTEM-GESUNDHEITSCHECK:\n\n"
                result += f"Status: {health['status'].upper()}\n\n"
                
                if health['alerts']:
                    result += "⚠️ PROBLEME GEFUNDEN:\n"
                    for alert in health['alerts']:
                        result += f"• {alert}\n"
                    result += "\n"
                
                if health['recommendations']:
                    result += "💡 EMPFEHLUNGEN:\n"
                    for rec in health['recommendations']:
                        result += f"• {rec}\n"
                    result += "\n"
                
                result += f"📊 {health['summary']}"
                return result
            except Exception as e:
                return f"❌ Fehler beim Health-Check: {e}"
        
        # === GIT-INTEGRATION BEFEHLE ===
        # Git-Repositories scannen
        if any(phrase in message_lower for phrase in ['git scan', 'scanne git', 'finde git repos']):
            try:
                repos = self.ai_handler.git_manager.scan_git_repositories()
                
                if not repos:
                    return "📂 Keine Git-Repositories gefunden"
                
                result = f"📁 GIT-REPOSITORIES ({len(repos)} gefunden):\n\n"
                for repo in repos[:10]:  # Erste 10
                    status_icon = {'clean': '✅', 'dirty': '⚠️', 'ahead': '⬆️', 'behind': '⬇️'}.get(repo['status'], '❓')
                    result += f"{status_icon} {repo['name']}\n"
                    result += f"   📍 {repo['path']}\n"
                    result += f"   🌿 {repo['branch']} | {repo['language']}\n"
                    if repo['uncommitted_changes']:
                        result += f"   ⚠️ Uncommitted changes\n"
                    if repo['commits_ahead'] > 0:
                        result += f"   ⬆️ {repo['commits_ahead']} ahead\n"
                    if repo['commits_behind'] > 0:
                        result += f"   ⬇️ {repo['commits_behind']} behind\n"
                    result += "\n"
                
                if len(repos) > 10:
                    result += f"... und {len(repos) - 10} weitere Repositories"
                
                return result
            except Exception as e:
                return f"❌ Fehler beim Git-Scan: {e}"
        
        # Git-Repository-Bericht
        if any(phrase in message_lower for phrase in ['git report', 'git bericht', 'git übersicht']):
            try:
                return self.ai_handler.git_manager.create_repository_report()
            except Exception as e:
                return f"❌ Fehler beim Git-Bericht: {e}"
        
        # Git-Status eines Repositories
        if message_lower.startswith('git status '):
            try:
                repo_path = message.split(' ', 2)[2] if len(message.split(' ')) > 2 else None
                if not repo_path:
                    return "❌ Bitte Repository-Pfad angeben: git status C:\\path\\to\\repo"
                
                return self.ai_handler.git_manager.get_repository_status(repo_path)
            except Exception as e:
                return f"❌ Fehler beim Git-Status: {e}"
        
        # Git-Commit & Push
        if message_lower.startswith('git commit '):
            try:
                parts = message.split(' ', 2)
                if len(parts) < 3:
                    return "❌ Format: git commit <pfad> [nachricht]"
                
                repo_path = parts[2].split(' ')[0]
                commit_msg = ' '.join(parts[2].split(' ')[1:]) if len(parts[2].split(' ')) > 1 else None
                
                return self.ai_handler.git_manager.auto_commit_push(repo_path, commit_msg)
            except Exception as e:
                return f"❌ Fehler beim Git-Commit: {e}"
        
        # Git-Pull
        if message_lower.startswith('git pull '):
            try:
                repo_path = message.split(' ', 2)[2] if len(message.split(' ')) > 2 else None
                if not repo_path:
                    return "❌ Bitte Repository-Pfad angeben: git pull C:\\path\\to\\repo"
                
                return self.ai_handler.git_manager.pull_latest(repo_path)
            except Exception as e:
                return f"❌ Fehler beim Git-Pull: {e}"
        
        # Git-Health-Check
        if any(phrase in message_lower for phrase in ['git health', 'git gesundheit']):
            try:
                health = self.ai_handler.git_manager.repository_health_check()
                
                result = f"🔧 GIT-REPOSITORIES GESUNDHEITSCHECK:\n\n"
                result += f"Status: {health['status'].upper()}\n"
                result += f"📂 {health['total_repositories']} Repositories\n\n"
                
                if health['issues']:
                    result += "⚠️ PROBLEME:\n"
                    for issue in health['issues']:
                        result += f"• {issue}\n"
                    result += "\n"
                
                if health['recommendations']:
                    result += "💡 EMPFEHLUNGEN:\n"
                    for rec in health['recommendations']:
                        result += f"• {rec}\n"
                
                return result
            except Exception as e:
                return f"❌ Fehler beim Git-Health-Check: {e}"
        
        # === TASK-SCHEDULER BEFEHLE ===
        # Task erstellen
        if message_lower.startswith('schedule ') or message_lower.startswith('plane task '):
            try:
                # Format: schedule "task name" "command" "schedule"
                parts = message.split('"')
                if len(parts) >= 6:
                    task_name = parts[1]
                    command = parts[3]
                    schedule_spec = parts[5]
                    
                    return self.ai_handler.task_scheduler.create_scheduled_task(
                        task_name, command, schedule_spec
                    )
                else:
                    return '❌ Format: schedule "Task Name" "command" "täglich 09:00"'
            except Exception as e:
                return f"❌ Fehler beim Task-Erstellen: {e}"
        
        # Tasks auflisten
        if any(phrase in message_lower for phrase in ['zeige tasks', 'list tasks', 'geplante tasks']):
            try:
                return self.ai_handler.task_scheduler.list_tasks()
            except Exception as e:
                return f"❌ Fehler beim Tasks-Auflisten: {e}"
        
        # Task löschen
        if message_lower.startswith('lösche task ') or message_lower.startswith('delete task '):
            try:
                task_name = message.split(' ', 2)[2]
                return self.ai_handler.task_scheduler.delete_task(task_name)
            except Exception as e:
                return f"❌ Fehler beim Task-Löschen: {e}"
        
        # Vordefinierte Automatisierung
        if message_lower.startswith('erstelle automation '):
            try:
                automation_type = message.split(' ', 2)[2]
                return self.ai_handler.task_scheduler.create_quick_automation(automation_type)
            except Exception as e:
                return f"❌ Fehler beim Erstellen der Automatisierung: {e}"
        
        # Automation-Regeln auflisten
        if any(phrase in message_lower for phrase in ['zeige automationen', 'list automations', 'automation regeln']):
            try:
                return self.ai_handler.task_scheduler.list_automation_rules()
            except Exception as e:
                return f"❌ Fehler beim Automation-Auflisten: {e}"
        
        # Scheduler-Status
        if any(phrase in message_lower for phrase in ['scheduler status', 'task scheduler status']):
            try:
                status = self.ai_handler.task_scheduler.get_scheduler_status()
                
                result = f"⚙️ TASK-SCHEDULER STATUS:\n\n"
                result += f"Status: {'🟢 Läuft' if status['running'] else '🔴 Gestoppt'}\n"
                result += f"📋 Tasks: {status['active_tasks']}/{status['total_tasks']} aktiv\n"
                result += f"🤖 Automation-Regeln: {status['active_rules']}/{status['total_rules']} aktiv\n"
                result += f"⏰ Geplante Jobs: {status['scheduled_jobs']}\n"
                
                return result
            except Exception as e:
                return f"❌ Fehler beim Scheduler-Status: {e}"
        
        # === HILFE-SYSTEM ===
        # Hilfe anzeigen
        if any(phrase in message_lower for phrase in ['hilfe', 'help', 'befehle', 'commands', 'was kannst du']):
            from ..core.command_reference import ToobixCommands
            cmd_ref = ToobixCommands()
            
            if any(word in message_lower for word in ['system', 'aufräum', 'cleanup']):
                return cmd_ref.get_category_help('system')
            elif any(word in message_lower for word in ['projekt', 'code', 'entwickl']):
                return cmd_ref.get_category_help('projects')
            elif any(word in message_lower for word in ['wissen', 'erinner', 'memory']):
                return cmd_ref.get_category_help('knowledge')
            elif any(word in message_lower for word in ['sprache', 'voice', 'sprechen']):
                return cmd_ref.get_category_help('speech')
            elif 'schnell' in message_lower or 'quick' in message_lower:
                return cmd_ref.get_quick_help()
            else:
                return cmd_ref.get_command_list()
        
        # Befehl suchen
        if message_lower.startswith('suche befehl ') or message_lower.startswith('finde befehl '):
            from ..core.command_reference import ToobixCommands
            cmd_ref = ToobixCommands()
            query = message_lower.replace('suche befehl ', '').replace('finde befehl ', '').strip()
            return cmd_ref.search_commands(query)
        
        # Datei suchen
        if any(word in message_lower for word in ['finde ', 'suche ', 'find ']):
            pattern = message_lower.replace('finde ', '').replace('suche ', '').replace('find ', '').strip()
            files = self.desktop.find_files(pattern)
            if files:
                file_list = '\n'.join([f"• {f}" for f in files[:10]])
                return f"🔍 Gefundene Dateien für '{pattern}':\n{file_list}"
            else:
                return f"❌ Keine Dateien gefunden für '{pattern}'"
        
        # Zeit/Datum
        if any(word in message_lower for word in ['wie spät', 'uhrzeit', 'zeit', 'datum']):
            current_time = self.desktop.get_current_time()
            return f"🕐 Es ist {current_time}"
        
        # System-Info
        if any(word in message_lower for word in ['system info', 'pc status', 'computer status']):
            info = self.desktop.get_system_info()
            return f"💻 System-Status:\nCPU: {info.get('cpu_usage', 'N/A')}\nRAM: {info.get('memory_usage', 'N/A')}\nFestplatte: {info.get('disk_usage', 'N/A')}"
        
        return None
    
    def _on_speech_command(self, command: str):
        """Callback für Sprachbefehle"""
        self.root.after(0, lambda: self._add_message("Du (Hey Toobix)", command))
        self._process_message(command)
    
    def _on_wake_word(self, text: str):
        """Callback für Wake-Word Detection"""
        self.root.after(0, lambda: self._update_status("👂 Wake-Word erkannt"))
    
    def _update_status(self, status: str):
        """Aktualisiert Status-Anzeige"""
        if hasattr(self, 'listening_status'):
            self.listening_status.configure(text=status)
    
    def _show_ai_status(self):
        """Zeigt AI-Status Dialog"""
        status = self.ai_handler.get_status()
        
        status_text = f"""AI Status:
        
Ollama: {'✅ Verfügbar' if status['ollama_available'] else '❌ Nicht verfügbar'}
Groq: {'✅ Verfügbar' if status['groq_available'] else '❌ Nicht verfügbar'}

Aktuelles Modell: {status['current_model']}
Letzte Antwortzeit: {status['last_response_time']:.1f}s
Fehler hintereinander: {status['consecutive_failures']}
        """
        
        messagebox.showinfo("Toobix AI Status", status_text)
    
    def _on_closing(self):
        """Behandelt Fenster schließen"""
        self.speech_engine.stop()
        self.root.destroy()
    
    def run(self):
        """Startet die GUI"""
        print("🎨 GUI gestartet - Toobix ist bereit!")
        self.root.mainloop()
