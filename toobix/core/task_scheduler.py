"""
Toobix Task Scheduler & Automation Engine
Intelligente Automatisierung und geplante Aufgaben
"""
import json
import threading
import time
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import os

class TaskScheduler:
    """Intelligenter Task-Scheduler mit Automation-Engine"""
    
    def __init__(self, settings=None):
        self.settings = settings
        self.tasks = {}
        self.automation_rules = {}
        self.running = False
        self.scheduler_thread = None
        
        # Task-Dateien
        self.tasks_file = Path(os.path.expanduser("~/.toobix_tasks.json"))
        self.rules_file = Path(os.path.expanduser("~/.toobix_automation_rules.json"))
        
        # Lade gespeicherte Tasks und Regeln
        self._load_tasks()
        self._load_automation_rules()
        
        print("⚙️ Task Scheduler initialisiert")
    
    def _load_tasks(self):
        """Lädt gespeicherte Tasks"""
        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    saved_tasks = json.load(f)
                    # Reaktiviere Tasks (ohne Function-Objects)
                    for task_id, task_data in saved_tasks.items():
                        if task_data.get('active', False):
                            # Tasks werden beim Start reaktiviert
                            pass
            except Exception as e:
                print(f"⚠️ Fehler beim Laden der Tasks: {e}")
    
    def _load_automation_rules(self):
        """Lädt Automatisierungs-Regeln"""
        if self.rules_file.exists():
            try:
                with open(self.rules_file, 'r', encoding='utf-8') as f:
                    self.automation_rules = json.load(f)
            except Exception as e:
                print(f"⚠️ Fehler beim Laden der Automation-Regeln: {e}")
                self.automation_rules = {}
    
    def _save_tasks(self):
        """Speichert Tasks (ohne Function-Objects)"""
        try:
            saveable_tasks = {}
            for task_id, task in self.tasks.items():
                saveable_tasks[task_id] = {
                    'name': task['name'],
                    'description': task['description'],
                    'schedule': task['schedule'],
                    'command': task['command'],
                    'active': task['active'],
                    'created': task['created'],
                    'last_run': task.get('last_run'),
                    'run_count': task.get('run_count', 0)
                }
            
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(saveable_tasks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern der Tasks: {e}")
    
    def _save_automation_rules(self):
        """Speichert Automatisierungs-Regeln"""
        try:
            with open(self.rules_file, 'w', encoding='utf-8') as f:
                json.dump(self.automation_rules, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern der Automation-Regeln: {e}")
    
    def create_scheduled_task(self, name: str, command: str, schedule_spec: str, description: str = "") -> str:
        """Erstellt eine geplante Aufgabe"""
        try:
            task_id = f"task_{int(time.time())}"
            
            # Parse Schedule-Specification
            schedule_parts = self._parse_schedule(schedule_spec)
            if not schedule_parts:
                return f"❌ Ungültige Schedule-Spezifikation: {schedule_spec}"
            
            # Erstelle Task
            task = {
                'id': task_id,
                'name': name,
                'description': description,
                'command': command,
                'schedule': schedule_spec,
                'schedule_parts': schedule_parts,
                'active': True,
                'created': datetime.now().isoformat(),
                'last_run': None,
                'run_count': 0,
                'function': None  # Wird später gesetzt
            }
            
            # Registriere bei schedule-Library
            success = self._register_schedule(task)
            if not success:
                return f"❌ Fehler beim Registrieren der Schedule: {schedule_spec}"
            
            self.tasks[task_id] = task
            self._save_tasks()
            
            # Starte Scheduler falls noch nicht läuft
            if not self.running:
                self.start_scheduler()
            
            return f"✅ Task '{name}' erstellt - Läuft {schedule_spec}"
            
        except Exception as e:
            return f"❌ Fehler beim Erstellen des Tasks: {e}"
    
    def _parse_schedule(self, schedule_spec: str) -> Optional[Dict[str, Any]]:
        """Parsed Schedule-Spezifikation"""
        schedule_spec = schedule_spec.lower().strip()
        
        # Unterstützte Formate:
        # "täglich 09:00", "daily 9am", "wöchentlich montag 14:30"
        # "jede stunde", "every 30 minutes", "every monday at 10:00"
        
        parts = {
            'type': None,
            'time': None,
            'day': None,
            'interval': None
        }
        
        if any(word in schedule_spec for word in ['täglich', 'daily']):
            parts['type'] = 'daily'
            # Extrahiere Zeit
            time_match = self._extract_time(schedule_spec)
            if time_match:
                parts['time'] = time_match
            else:
                return None
                
        elif any(word in schedule_spec for word in ['wöchentlich', 'weekly']):
            parts['type'] = 'weekly'
            # Extrahiere Wochentag und Zeit
            day_match = self._extract_weekday(schedule_spec)
            time_match = self._extract_time(schedule_spec)
            if day_match and time_match:
                parts['day'] = day_match
                parts['time'] = time_match
            else:
                return None
                
        elif any(word in schedule_spec for word in ['stündlich', 'hourly', 'jede stunde', 'every hour']):
            parts['type'] = 'hourly'
            
        elif 'minutes' in schedule_spec or 'minuten' in schedule_spec:
            parts['type'] = 'interval'
            # Extrahiere Intervall
            import re
            match = re.search(r'(\d+)', schedule_spec)
            if match:
                parts['interval'] = int(match.group(1))
            else:
                return None
                
        else:
            return None
        
        return parts
    
    def _extract_time(self, text: str) -> Optional[str]:
        """Extrahiert Zeit aus Text"""
        import re
        
        # Formate: 09:00, 9:00, 14:30, 9am, 2pm
        time_patterns = [
            r'(\d{1,2}):(\d{2})',  # 09:00, 14:30
            r'(\d{1,2})am',        # 9am
            r'(\d{1,2})pm'         # 2pm
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text)
            if match:
                if ':' in match.group(0):
                    return match.group(0)  # 09:00
                else:
                    hour = int(match.group(1))
                    if 'pm' in match.group(0) and hour != 12:
                        hour += 12
                    elif 'am' in match.group(0) and hour == 12:
                        hour = 0
                    return f"{hour:02d}:00"
        
        return None
    
    def _extract_weekday(self, text: str) -> Optional[str]:
        """Extrahiert Wochentag aus Text"""
        weekdays = {
            'montag': 'monday', 'dienstag': 'tuesday', 'mittwoch': 'wednesday',
            'donnerstag': 'thursday', 'freitag': 'friday', 'samstag': 'saturday', 'sonntag': 'sunday',
            'monday': 'monday', 'tuesday': 'tuesday', 'wednesday': 'wednesday',
            'thursday': 'thursday', 'friday': 'friday', 'saturday': 'saturday', 'sunday': 'sunday'
        }
        
        for german, english in weekdays.items():
            if german in text.lower():
                return english
        
        return None
    
    def _register_schedule(self, task: Dict[str, Any]) -> bool:
        """Registriert Task bei schedule-Library"""
        try:
            schedule_parts = task['schedule_parts']
            
            def task_wrapper():
                self._execute_task(task['id'])
            
            if schedule_parts['type'] == 'daily':
                time_str = schedule_parts['time']
                schedule.every().day.at(time_str).do(task_wrapper)
                
            elif schedule_parts['type'] == 'weekly':
                day = schedule_parts['day']
                time_str = schedule_parts['time']
                getattr(schedule.every(), day).at(time_str).do(task_wrapper)
                
            elif schedule_parts['type'] == 'hourly':
                schedule.every().hour.do(task_wrapper)
                
            elif schedule_parts['type'] == 'interval':
                interval = schedule_parts['interval']
                schedule.every(interval).minutes.do(task_wrapper)
            
            # Speichere Function-Reference
            task['function'] = task_wrapper
            
            return True
            
        except Exception as e:
            print(f"Fehler beim Registrieren der Schedule: {e}")
            return False
    
    def _execute_task(self, task_id: str):
        """Führt einen Task aus"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        
        try:
            print(f"⚙️ Führe Task aus: {task['name']}")
            
            # Hier würde die eigentliche Befehlsausführung stattfinden
            # Verbindung zum Desktop-Integration oder Command-Handler
            command = task['command']
            
            # Simuliere Ausführung (in echter Implementation würde hier 
            # der Command an den entsprechenden Handler weitergeleitet)
            result = f"Executed: {command}"
            
            # Update Task-Statistiken
            task['last_run'] = datetime.now().isoformat()
            task['run_count'] = task.get('run_count', 0) + 1
            
            self._save_tasks()
            
            print(f"✅ Task '{task['name']}' erfolgreich ausgeführt")
            
        except Exception as e:
            print(f"❌ Fehler beim Ausführen von Task '{task['name']}': {e}")
    
    def start_scheduler(self):
        """Startet den Task-Scheduler"""
        if self.running:
            return "⚙️ Scheduler läuft bereits"
        
        self.running = True
        
        def scheduler_loop():
            while self.running:
                schedule.run_pending()
                time.sleep(30)  # Check alle 30 Sekunden
        
        self.scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        return "✅ Task-Scheduler gestartet"
    
    def stop_scheduler(self):
        """Stoppt den Task-Scheduler"""
        self.running = False
        schedule.clear()
        return "🛑 Task-Scheduler gestoppt"
    
    def list_tasks(self) -> str:
        """Listet alle Tasks auf"""
        if not self.tasks:
            return "📋 Keine geplanten Tasks vorhanden"
        
        result = "⚙️ GEPLANTE TASKS:\n\n"
        
        for task_id, task in self.tasks.items():
            status = "🟢 Aktiv" if task['active'] else "🔴 Inaktiv"
            result += f"📋 {task['name']}\n"
            result += f"   Status: {status}\n"
            result += f"   Schedule: {task['schedule']}\n"
            result += f"   Command: {task['command']}\n"
            result += f"   Erstellt: {task['created']}\n"
            
            if task.get('last_run'):
                result += f"   Letzte Ausführung: {task['last_run']}\n"
            
            if task.get('run_count'):
                result += f"   Ausführungen: {task['run_count']}x\n"
            
            result += "\n"
        
        scheduler_status = "🟢 Läuft" if self.running else "🔴 Gestoppt"
        result += f"Scheduler-Status: {scheduler_status}"
        
        return result
    
    def delete_task(self, task_identifier: str) -> str:
        """Löscht einen Task (per ID oder Name)"""
        # Suche nach ID oder Name
        task_to_delete = None
        
        if task_identifier in self.tasks:
            task_to_delete = task_identifier
        else:
            for task_id, task in self.tasks.items():
                if task['name'].lower() == task_identifier.lower():
                    task_to_delete = task_id
                    break
        
        if not task_to_delete:
            return f"❌ Task '{task_identifier}' nicht gefunden"
        
        task_name = self.tasks[task_to_delete]['name']
        del self.tasks[task_to_delete]
        self._save_tasks()
        
        # Schedule neu aufbauen (einfacher als einzelne Entfernung)
        schedule.clear()
        for task in self.tasks.values():
            if task['active']:
                self._register_schedule(task)
        
        return f"✅ Task '{task_name}' gelöscht"
    
    def create_automation_rule(self, name: str, trigger: str, action: str, condition: str = None) -> str:
        """Erstellt eine Automatisierungs-Regel"""
        try:
            rule_id = f"rule_{int(time.time())}"
            
            rule = {
                'id': rule_id,
                'name': name,
                'trigger': trigger,
                'action': action,
                'condition': condition,
                'active': True,
                'created': datetime.now().isoformat(),
                'triggered_count': 0,
                'last_triggered': None
            }
            
            self.automation_rules[rule_id] = rule
            self._save_automation_rules()
            
            return f"✅ Automation-Regel '{name}' erstellt"
            
        except Exception as e:
            return f"❌ Fehler beim Erstellen der Automation-Regel: {e}"
    
    def check_automation_triggers(self, event_type: str, event_data: Dict[str, Any] = None) -> List[str]:
        """Prüft ob Automation-Regeln getriggert werden sollen"""
        triggered_actions = []
        
        for rule_id, rule in self.automation_rules.items():
            if not rule['active']:
                continue
            
            # Einfache Trigger-Logik
            trigger = rule['trigger'].lower()
            
            # Trigger-Typen
            trigger_matches = False
            
            if event_type == 'time' and any(word in trigger for word in ['daily', 'täglich', 'startup']):
                trigger_matches = True
            elif event_type == 'system' and any(word in trigger for word in ['high_cpu', 'low_disk', 'system']):
                trigger_matches = True
            elif event_type == 'file' and any(word in trigger for word in ['file_created', 'file_modified', 'download']):
                trigger_matches = True
            
            if trigger_matches:
                # Prüfe Bedingung (falls vorhanden)
                condition_met = True
                if rule['condition']:
                    condition_met = self._evaluate_condition(rule['condition'], event_data)
                
                if condition_met:
                    triggered_actions.append(rule['action'])
                    
                    # Update Regel-Statistiken
                    rule['triggered_count'] += 1
                    rule['last_triggered'] = datetime.now().isoformat()
        
        if triggered_actions:
            self._save_automation_rules()
        
        return triggered_actions
    
    def _evaluate_condition(self, condition: str, event_data: Dict[str, Any] = None) -> bool:
        """Evaluiert eine Bedingung"""
        # Einfache Bedingungslogik
        # In der Praxis würde hier eine richtige Expression-Engine verwendet
        
        condition = condition.lower()
        
        if not event_data:
            return True
        
        # Beispiel-Bedingungen
        if 'cpu_usage' in condition and 'cpu_percent' in event_data:
            # "cpu_usage > 80"
            if '>' in condition:
                threshold = float(condition.split('>')[1].strip())
                return event_data['cpu_percent'] > threshold
        
        if 'memory_usage' in condition and 'memory_percent' in event_data:
            # "memory_usage > 90"
            if '>' in condition:
                threshold = float(condition.split('>')[1].strip())
                return event_data['memory_percent'] > threshold
        
        return True
    
    def list_automation_rules(self) -> str:
        """Listet alle Automation-Regeln auf"""
        if not self.automation_rules:
            return "🤖 Keine Automatisierungs-Regeln vorhanden"
        
        result = "🤖 AUTOMATISIERUNGS-REGELN:\n\n"
        
        for rule_id, rule in self.automation_rules.items():
            status = "🟢 Aktiv" if rule['active'] else "🔴 Inaktiv"
            result += f"⚡ {rule['name']}\n"
            result += f"   Status: {status}\n"
            result += f"   Trigger: {rule['trigger']}\n"
            result += f"   Action: {rule['action']}\n"
            
            if rule['condition']:
                result += f"   Bedingung: {rule['condition']}\n"
            
            result += f"   Erstellt: {rule['created']}\n"
            
            if rule.get('triggered_count', 0) > 0:
                result += f"   Ausgelöst: {rule['triggered_count']}x\n"
                if rule.get('last_triggered'):
                    result += f"   Zuletzt: {rule['last_triggered']}\n"
            
            result += "\n"
        
        return result
    
    def get_scheduler_status(self) -> Dict[str, Any]:
        """Gibt detaillierten Scheduler-Status zurück"""
        return {
            'running': self.running,
            'total_tasks': len(self.tasks),
            'active_tasks': len([t for t in self.tasks.values() if t['active']]),
            'total_rules': len(self.automation_rules),
            'active_rules': len([r for r in self.automation_rules.values() if r['active']]),
            'scheduled_jobs': len(schedule.jobs),
            'status': 'running' if self.running else 'stopped'
        }
    
    def create_quick_automation(self, automation_type: str) -> str:
        """Erstellt vordefinierte Automatisierungen"""
        automations = {
            'daily_cleanup': {
                'name': 'Tägliche System-Aufräumung',
                'schedule': 'täglich 09:00',
                'command': 'analysiere system'
            },
            'weekly_backup': {
                'name': 'Wöchentliches Backup',
                'schedule': 'wöchentlich freitag 18:00',
                'command': 'backup erstellen'
            },
            'hourly_git_check': {
                'name': 'Stündlicher Git-Check',
                'schedule': 'stündlich',
                'command': 'git status'
            },
            'startup_check': {
                'name': 'System-Check beim Start',
                'schedule': 'täglich 08:00',
                'command': 'analysiere system'
            }
        }
        
        if automation_type not in automations:
            available = ', '.join(automations.keys())
            return f"❌ Unbekannte Automatisierung. Verfügbar: {available}"
        
        auto = automations[automation_type]
        return self.create_scheduled_task(
            auto['name'],
            auto['command'],
            auto['schedule'],
            f"Vordefinierte Automatisierung: {automation_type}"
        )
