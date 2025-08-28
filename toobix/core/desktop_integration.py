"""
Toobix Desktop Integration
Windows-Systemintegration, Dateiverwaltung und Automation
"""
import os
import subprocess
import psutil
import pygetwindow as gw
import pyautogui
import keyboard
import time
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Any
from toobix.core.system_organizer import SystemOrganizer

class DesktopIntegration:
    """Verwaltet Windows Desktop-Integration und Automation"""
    
    def __init__(self):
        self.common_programs = self._load_common_programs()
        self.organizer = SystemOrganizer(None)  # Wird später mit settings initialisiert
        print("🖥️ Desktop Integration initialisiert")
    
    def _load_common_programs(self) -> Dict[str, str]:
        """Lädt häufig verwendete Programme"""
        programs = {
            # Text-Editoren
            'notepad': 'notepad.exe',
            'editor': 'notepad.exe',
            'texteditor': 'notepad.exe',
            
            # Browser
            'browser': 'msedge.exe',
            'edge': 'msedge.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            
            # Office
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe',
            
            # System
            'explorer': 'explorer.exe',
            'calculator': 'calc.exe',
            'rechner': 'calc.exe',
            'taskmanager': 'taskmgr.exe',
            'paint': 'mspaint.exe',
            
            # Entwicklung
            'vscode': 'code.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'terminal': 'wt.exe'
        }
        return programs
    
    # === PROGRAMM-STEUERUNG ===
    
    def open_program(self, program_name: str) -> bool:
        """Öffnet ein Programm"""
        try:
            program_name = program_name.lower().strip()
            
            # Direkte Programm-Namen prüfen
            if program_name in self.common_programs:
                executable = self.common_programs[program_name]
                subprocess.Popen(executable, shell=True)
                print(f"✅ Programm geöffnet: {program_name}")
                return True
            
            # Versuche direkten Start
            try:
                subprocess.Popen(program_name, shell=True)
                print(f"✅ Programm geöffnet: {program_name}")
                return True
            except:
                pass
            
            # Windows Start-Menü durchsuchen
            if self._open_via_start_menu(program_name):
                return True
            
            print(f"❌ Programm nicht gefunden: {program_name}")
            return False
            
        except Exception as e:
            print(f"❌ Fehler beim Öffnen von {program_name}: {e}")
            return False
    
    def _open_via_start_menu(self, program_name: str) -> bool:
        """Versucht Programm über Start-Menü zu öffnen"""
        try:
            # Windows-Taste drücken
            pyautogui.press('win')
            time.sleep(0.5)
            
            # Programm-Name tippen
            pyautogui.write(program_name)
            time.sleep(1)
            
            # Enter drücken
            pyautogui.press('enter')
            time.sleep(0.5)
            
            print(f"🔍 Versuche Start-Menü: {program_name}")
            return True
            
        except Exception as e:
            print(f"❌ Start-Menü Fehler: {e}")
            return False
    
    def close_program(self, program_name: str) -> bool:
        """Schließt ein Programm"""
        try:
            program_name = program_name.lower()
            closed_count = 0
            
            # Alle Prozesse durchsuchen
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if program_name in proc.info['name'].lower():
                        proc.terminate()
                        closed_count += 1
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if closed_count > 0:
                print(f"✅ {closed_count} Instanz(en) von {program_name} geschlossen")
                return True
            else:
                print(f"❌ Programm nicht gefunden: {program_name}")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Schließen von {program_name}: {e}")
            return False
    
    def get_running_programs(self) -> List[str]:
        """Gibt Liste laufender Programme zurück"""
        try:
            programs = set()
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name']
                    if name and not name.startswith('System'):
                        programs.add(name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return sorted(list(programs))
            
        except Exception as e:
            print(f"❌ Fehler beim Abrufen der Programme: {e}")
            return []
    
    # === DATEI-VERWALTUNG ===
    
    def find_files(self, pattern: str, directory: Optional[str] = None) -> List[str]:
        """Sucht Dateien nach Pattern"""
        try:
            if directory is None:
                # Standard-Verzeichnisse durchsuchen
                search_dirs = [
                    os.path.expanduser("~/Desktop"),
                    os.path.expanduser("~/Downloads"),
                    os.path.expanduser("~/Documents"),
                    "C:/Users/Public/Desktop"
                ]
            else:
                search_dirs = [directory]
            
            found_files = []
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for root, dirs, files in os.walk(search_dir):
                        for file in files:
                            if pattern.lower() in file.lower():
                                found_files.append(os.path.join(root, file))
                        
                        # Nicht zu tief suchen (Performance)
                        if len(root.split(os.sep)) > len(search_dir.split(os.sep)) + 3:
                            dirs.clear()
            
            print(f"🔍 {len(found_files)} Datei(en) gefunden für: {pattern}")
            return found_files[:20]  # Maximal 20 Ergebnisse
            
        except Exception as e:
            print(f"❌ Dateisuch-Fehler: {e}")
            return []
    
    def open_file(self, file_path: str) -> bool:
        """Öffnet eine Datei"""
        try:
            if os.path.exists(file_path):
                os.startfile(file_path)
                print(f"✅ Datei geöffnet: {file_path}")
                return True
            else:
                print(f"❌ Datei nicht gefunden: {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Öffnen der Datei: {e}")
            return False
    
    def create_file(self, file_path: str, content: str = "") -> bool:
        """Erstellt eine neue Datei"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Datei erstellt: {file_path}")
            return True
            
        except Exception as e:
            print(f"❌ Fehler beim Erstellen der Datei: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """Löscht eine Datei (in Papierkorb)"""
        try:
            if os.path.exists(file_path):
                # Sicherheitsabfrage könnte hier implementiert werden
                send2trash.send2trash(file_path)  # Benötigt send2trash package
                print(f"🗑️ Datei gelöscht: {file_path}")
                return True
            else:
                print(f"❌ Datei nicht gefunden: {file_path}")
                return False
                
        except Exception as e:
            # Fallback: Normale Löschung
            try:
                os.remove(file_path)
                print(f"🗑️ Datei gelöscht: {file_path}")
                return True
            except:
                print(f"❌ Fehler beim Löschen der Datei: {e}")
                return False
    
    # === SYSTEM-INFORMATION ===
    
    def get_system_info(self) -> Dict[str, Any]:
        """Gibt System-Informationen zurück"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('C:/')
            
            return {
                'cpu_usage': f"{cpu_percent}%",
                'memory_usage': f"{memory.percent}%",
                'disk_usage': f"{disk.percent}%",
                'memory_available': f"{memory.available // (1024**3)} GB",
                'disk_free': f"{disk.free // (1024**3)} GB"
            }
            
        except Exception as e:
            print(f"❌ System-Info Fehler: {e}")
            return {}
    
    def get_current_time(self) -> str:
        """Gibt aktuelle Zeit zurück"""
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S, %d.%m.%Y")
    
    # === FENSTER-VERWALTUNG ===
    
    def get_active_window(self) -> Optional[str]:
        """Gibt aktives Fenster zurück"""
        try:
            active = gw.getActiveWindow()
            if active:
                return active.title
            return None
        except Exception as e:
            print(f"❌ Fenster-Info Fehler: {e}")
            return None
    
    def list_windows(self) -> List[str]:
        """Gibt alle offenen Fenster zurück"""
        try:
            windows = []
            for window in gw.getAllWindows():
                if window.title and window.title.strip():
                    windows.append(window.title)
            return windows
        except Exception as e:
            print(f"❌ Fenster-Liste Fehler: {e}")
            return []
    
    # === AUTOMATION HELPERS ===
    
    def execute_command(self, command: str) -> str:
        """Führt System-Kommando aus"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Fehler: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return "Timeout: Kommando dauerte zu lange"
        except Exception as e:
            return f"Fehler beim Ausführen: {e}"
    
    # === SYSTEM AUFRÄUMUNG ===
    
    def analyze_system_cleanliness(self) -> str:
        """Analysiert das System und gibt Aufräum-Empfehlungen"""
        try:
            analysis = self.organizer.analyze_system_mess()
            
            report = "🔍 SYSTEM-ANALYSE:\n\n"
            
            # Festplatten-Status
            if analysis['disk_usage']:
                report += "💾 FESTPLATTEN-NUTZUNG:\n"
                for device, usage in analysis['disk_usage'].items():
                    status = "⚠️" if usage['percent_used'] > 85 else "✅"
                    report += f"{status} {device}: {usage['percent_used']}% belegt ({usage['free_gb']} GB frei)\n"
                report += "\n"
            
            # Aufräum-Möglichkeiten
            if analysis['recommendations']:
                report += "🧹 AUFRÄUM-EMPFEHLUNGEN:\n"
                for rec in analysis['recommendations']:
                    report += f"• {rec}\n"
                report += "\n"
            
            # Details
            if analysis['old_downloads']:
                report += f"📁 {len(analysis['old_downloads'])} alte Downloads gefunden\n"
            
            if analysis['temp_files']:
                temp_size = sum(f['size_mb'] for f in analysis['temp_files'])
                report += f"🗑️ {temp_size:.1f} MB temporäre Dateien\n"
            
            if analysis['large_files']:
                large_size = sum(f['size_gb'] for f in analysis['large_files'])
                report += f"📊 {large_size:.1f} GB in großen Dateien\n"
            
            if not analysis['recommendations']:
                report += "✨ Dein System ist bereits gut organisiert!"
            
            return report
            
        except Exception as e:
            return f"❌ Fehler bei der System-Analyse: {e}"
    
    def create_cleanup_plan(self) -> str:
        """Erstellt einen sicheren Aufräumplan"""
        try:
            analysis = self.organizer.analyze_system_mess()
            plan = self.organizer.create_safe_cleanup_plan(analysis)
            
            report = "📋 SICHERER AUFRÄUMPLAN:\n\n"
            report += f"🛡️ Sicherheitsstufe: {plan['safety_level']}\n"
            report += f"💾 Geschätzter Speichergewinn: {plan['estimated_space_gb']:.2f} GB\n\n"
            
            if plan['backup_recommended']:
                report += "⚠️ BACKUP EMPFOHLEN vor Ausführung!\n\n"
            
            report += "📋 GEPLANTE AKTIONEN:\n"
            for i, action in enumerate(plan['actions'], 1):
                report += f"{i}. {action['description']}\n"
                report += f"   🛡️ Sicherheit: {action['safety']}\n"
                report += f"   🔄 Rückgängig machbar: {'Ja' if action['reversible'] else 'Nein'}\n"
                if 'space_saved_gb' in action:
                    report += f"   💾 Speicher: {action['space_saved_gb']:.2f} GB\n"
                report += "\n"
            
            report += "💡 Verwende 'toobix backup erstellen' vor dem Aufräumen!\n"
            report += "💡 Verwende 'toobix aufräumen starten' zum Ausführen!"
            
            return report
            
        except Exception as e:
            return f"❌ Fehler beim Erstellen des Aufräumplans: {e}"
    
    def execute_cleanup(self, confirm: bool = False) -> str:
        """Führt sichere System-Aufräumung aus"""
        try:
            if not confirm:
                return "⚠️ Sicherheitsabfrage: Füge 'bestätigt' zum Befehl hinzu um fortzufahren!\nBeispiel: 'toobix aufräumen starten bestätigt'"
            
            analysis = self.organizer.analyze_system_mess()
            plan = self.organizer.create_safe_cleanup_plan(analysis)
            
            # Erst Dry-Run
            dry_results = self.organizer.execute_safe_cleanup(plan, dry_run=True)
            
            report = "🧪 AUFRÄUMUNG SIMULATION:\n\n"
            report += f"✅ {len(dry_results['completed_actions'])} Aktionen simuliert\n"
            report += f"❌ {len(dry_results['failed_actions'])} Fehler\n"
            report += f"💾 Geschätzter Speichergewinn: {dry_results['space_freed_gb']:.2f} GB\n\n"
            
            # Echte Ausführung
            real_results = self.organizer.execute_safe_cleanup(plan, dry_run=False)
            
            report += "🔄 ECHTE AUSFÜHRUNG:\n\n"
            report += f"✅ {len(real_results['completed_actions'])} Aktionen erfolgreich\n"
            report += f"❌ {len(real_results['failed_actions'])} Fehler\n"
            report += f"💾 Tatsächlich freigegebener Speicher: {real_results['space_freed_gb']:.2f} GB\n\n"
            
            if real_results['completed_actions']:
                report += "📋 AUSGEFÜHRTE AKTIONEN:\n"
                for action in real_results['completed_actions']:
                    report += f"• {action['action']}: "
                    if 'deleted_files' in action:
                        report += f"{action['deleted_files']} Dateien gelöscht\n"
                    elif 'moved_files' in action:
                        report += f"{action['moved_files']} Dateien verschoben\n"
                    elif 'organized_files' in action:
                        report += f"{action['organized_files']} Dateien organisiert\n"
            
            if real_results['failed_actions']:
                report += "\n❌ FEHLER:\n"
                for error in real_results['failed_actions']:
                    report += f"• {error.get('action', 'Unbekannt')}: {error.get('error', 'Unbekannter Fehler')}\n"
            
            report += "\n✨ Aufräumung abgeschlossen!"
            
            return report
            
        except Exception as e:
            return f"❌ Fehler bei der Aufräumung: {e}"
    
    def create_backup(self) -> str:
        """Erstellt Backup wichtiger Dateien"""
        try:
            backup_info = self.organizer.create_backup_important_files()
            
            report = "💾 BACKUP ERSTELLT:\n\n"
            report += f"📁 Backup-Ort: {backup_info['backup_location']}\n"
            report += f"💾 Gesamtgröße: {backup_info['total_size_gb']:.2f} GB\n\n"
            
            report += "📋 GESICHERTE ORDNER:\n"
            for backup in backup_info['backed_up_dirs']:
                report += f"• {backup['source']} → {backup['size_gb']:.2f} GB\n"
            
            report += "\n✅ Backup erfolgreich erstellt!"
            report += "\n💡 Du kannst jetzt sicher aufräumen!"
            
            return report
            
        except Exception as e:
            return f"❌ Fehler beim Backup: {e}"
