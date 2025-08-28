"""
Toobix Intelligent Task Scheduler & Automation Engine
Fortgeschrittene Automatisierung mit Event-basierter Regelausführung
"""

import schedule
import time
import threading
import json
import subprocess
import os
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Optional, Any
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
from enum import Enum

class TriggerType(Enum):
    """Verfügbare Trigger-Typen"""
    TIME = "time"
    FILE_CHANGE = "file_change"
    SYSTEM_EVENT = "system_event"
    PROCESS_EVENT = "process_event"
    MANUAL = "manual"

class ActionType(Enum):
    """Verfügbare Action-Typen"""
    COMMAND = "command"
    SCRIPT = "script"
    FUNCTION = "function"
    NOTIFICATION = "notification"

@dataclass
class AutomationRule:
    """Automatisierungs-Regel Definition"""
    id: str
    name: str
    description: str
    trigger_type: TriggerType
    trigger_config: Dict
    action_type: ActionType
    action_config: Dict
    enabled: bool = True
    created_at: str = None
    last_executed: str = None
    execution_count: int = 0
    success_count: int = 0
    error_count: int = 0

class IntelligentTaskScheduler:
    """Intelligenter Task-Scheduler mit Event-basierter Automatisierung"""
    
    def __init__(self, settings=None):
        self.settings = settings
        self.automation_rules = {}
        self.scheduled_jobs = {}
        self.running = False
        self.scheduler_thread = None
        self.file_watchers = {}
        self.system_monitors = {}
        self.logger = logging.getLogger('IntelligentTaskScheduler')
        
        # Standard-Pfade
        self.config_file = Path('toobix_automation_rules.json')
        self.scripts_dir = Path('toobix_scripts')
        self.scripts_dir.mkdir(exist_ok=True)
        
        # Action-Handler
        self.action_handlers = {
            ActionType.COMMAND: self._execute_command,
            ActionType.SCRIPT: self._execute_script,
            ActionType.FUNCTION: self._execute_function,
            ActionType.NOTIFICATION: self._send_notification
        }
        
        # Lade gespeicherte Regeln
        self.load_automation_rules()
        
    def start_scheduler(self) -> None:
        """Startet den Task-Scheduler"""
        if self.running:
            return
            
        self.running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("Intelligent Task Scheduler gestartet")
        
    def stop_scheduler(self) -> None:
        """Stoppt den Task-Scheduler"""
        self.running = False
        schedule.clear()
        self.logger.info("Intelligent Task Scheduler gestoppt")
        
    def _scheduler_loop(self) -> None:
        """Haupt-Scheduler-Loop"""
        while self.running:
            try:
                schedule.run_pending()
                self._check_file_watchers()
                self._check_system_events()
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Fehler im Scheduler-Loop: {e}")
                time.sleep(5)
                
    def create_automation_rule(self, rule_data: Dict) -> str:
        """Erstellt neue Automatisierungs-Regel"""
        try:
            rule_id = f"rule_{int(time.time())}_{len(self.automation_rules)}"
            
            rule = AutomationRule(
                id=rule_id,
                name=rule_data['name'],
                description=rule_data.get('description', ''),
                trigger_type=TriggerType(rule_data['trigger_type']),
                trigger_config=rule_data['trigger_config'],
                action_type=ActionType(rule_data['action_type']),
                action_config=rule_data['action_config'],
                enabled=rule_data.get('enabled', True),
                created_at=datetime.now().isoformat()
            )
            
            self.automation_rules[rule_id] = rule
            self._setup_rule_trigger(rule)
            self.save_automation_rules()
            
            self.logger.info(f"Automatisierungs-Regel erstellt: {rule.name}")
            return rule_id
            
        except Exception as e:
            self.logger.error(f"Fehler beim Erstellen der Automatisierungs-Regel: {e}")
            raise
            
    def _setup_rule_trigger(self, rule: AutomationRule) -> None:
        """Richtet Trigger für Regel ein"""
        try:
            if rule.trigger_type == TriggerType.TIME:
                self._setup_time_trigger(rule)
            elif rule.trigger_type == TriggerType.FILE_CHANGE:
                self._setup_file_watcher(rule)
            elif rule.trigger_type == TriggerType.SYSTEM_EVENT:
                self._setup_system_monitor(rule)
            elif rule.trigger_type == TriggerType.PROCESS_EVENT:
                self._setup_process_monitor(rule)
                
        except Exception as e:
            self.logger.error(f"Fehler beim Einrichten des Triggers für {rule.name}: {e}")
            
    def _setup_time_trigger(self, rule: AutomationRule) -> None:
        """Richtet zeitbasierten Trigger ein"""
        config = rule.trigger_config
        
        def job_function():
            self._execute_rule(rule)
            
        if 'interval' in config:
            # Intervall-basiert (z.B. alle 30 Minuten)
            interval = config['interval']
            unit = config.get('unit', 'minutes')
            
            if unit == 'seconds':
                schedule.every(interval).seconds.do(job_function)
            elif unit == 'minutes':
                schedule.every(interval).minutes.do(job_function)
            elif unit == 'hours':
                schedule.every(interval).hours.do(job_function)
            elif unit == 'days':
                schedule.every(interval).days.do(job_function)
                
        elif 'time' in config:
            # Spezifische Zeit (z.B. 14:30)
            schedule.every().day.at(config['time']).do(job_function)
            
        elif 'cron' in config:
            # Cron-ähnliche Syntax (vereinfacht)
            cron_expr = config['cron']
            if cron_expr == 'daily':
                schedule.every().day.at("00:00").do(job_function)
            elif cron_expr == 'weekly':
                schedule.every().week.do(job_function)
            elif cron_expr == 'monthly':
                schedule.every().month.do(job_function)
                
    def _setup_file_watcher(self, rule: AutomationRule) -> None:
        """Richtet Datei-Überwachung ein"""
        config = rule.trigger_config
        watch_path = Path(config['path'])
        
        if rule.id not in self.file_watchers:
            self.file_watchers[rule.id] = {
                'path': watch_path,
                'last_modified': {},
                'rule': rule
            }
            
    def _check_file_watchers(self) -> None:
        """Prüft Datei-Watcher auf Änderungen"""
        for watcher_id, watcher in self.file_watchers.items():
            try:
                watch_path = watcher['path']
                rule = watcher['rule']
                
                if not watch_path.exists():
                    continue
                    
                if watch_path.is_file():
                    # Einzelne Datei überwachen
                    current_mtime = watch_path.stat().st_mtime
                    last_mtime = watcher['last_modified'].get(str(watch_path), 0)
                    
                    if current_mtime > last_mtime:
                        watcher['last_modified'][str(watch_path)] = current_mtime
                        self._execute_rule(rule, {'changed_file': str(watch_path)})
                        
                elif watch_path.is_dir():
                    # Verzeichnis überwachen
                    config = rule.trigger_config
                    pattern = config.get('pattern', '*')
                    
                    for file_path in watch_path.glob(pattern):
                        if file_path.is_file():
                            current_mtime = file_path.stat().st_mtime
                            last_mtime = watcher['last_modified'].get(str(file_path), 0)
                            
                            if current_mtime > last_mtime:
                                watcher['last_modified'][str(file_path)] = current_mtime
                                self._execute_rule(rule, {'changed_file': str(file_path)})
                                
            except Exception as e:
                self.logger.error(f"Fehler beim File-Watching {watcher_id}: {e}")
                
    def _setup_system_monitor(self, rule: AutomationRule) -> None:
        """Richtet System-Event-Überwachung ein"""
        config = rule.trigger_config
        
        self.system_monitors[rule.id] = {
            'event_type': config['event_type'],
            'threshold': config.get('threshold'),
            'rule': rule,
            'last_check': time.time()
        }
        
    def _check_system_events(self) -> None:
        """Prüft System-Events"""
        import psutil
        
        for monitor_id, monitor in self.system_monitors.items():
            try:
                rule = monitor['rule']
                event_type = monitor['event_type']
                threshold = monitor['threshold']
                
                # CPU-Überwachung
                if event_type == 'cpu_high':
                    cpu_percent = psutil.cpu_percent(interval=1)
                    if cpu_percent > threshold:
                        self._execute_rule(rule, {'cpu_percent': cpu_percent})
                        
                # Memory-Überwachung
                elif event_type == 'memory_high':
                    memory = psutil.virtual_memory()
                    if memory.percent > threshold:
                        self._execute_rule(rule, {'memory_percent': memory.percent})
                        
                # Disk-Überwachung
                elif event_type == 'disk_full':
                    for partition in psutil.disk_partitions():
                        try:
                            usage = psutil.disk_usage(partition.mountpoint)
                            usage_percent = (usage.used / usage.total) * 100
                            if usage_percent > threshold:
                                self._execute_rule(rule, {
                                    'disk_usage': usage_percent,
                                    'partition': partition.device
                                })
                        except PermissionError:
                            continue
                            
            except Exception as e:
                self.logger.error(f"Fehler beim System-Monitoring {monitor_id}: {e}")
                
    def _execute_rule(self, rule: AutomationRule, context: Dict = None) -> Dict:
        """Führt Automatisierungs-Regel aus"""
        if not rule.enabled:
            return {'success': False, 'message': 'Rule disabled'}
            
        try:
            self.logger.info(f"Executing rule: {rule.name}")
            
            # Action ausführen
            handler = self.action_handlers.get(rule.action_type)
            if not handler:
                raise ValueError(f"Unknown action type: {rule.action_type}")
                
            result = handler(rule.action_config, context or {})
            
            # Statistiken aktualisieren
            rule.execution_count += 1
            rule.last_executed = datetime.now().isoformat()
            
            if result.get('success', False):
                rule.success_count += 1
            else:
                rule.error_count += 1
                
            self.save_automation_rules()
            
            return result
            
        except Exception as e:
            rule.error_count += 1
            self.logger.error(f"Fehler beim Ausführen der Regel {rule.name}: {e}")
            return {'success': False, 'error': str(e)}
            
    def _execute_command(self, config: Dict, context: Dict) -> Dict:
        """Führt System-Kommando aus"""
        try:
            command = config['command']
            
            # Template-Variablen ersetzen
            for key, value in context.items():
                command = command.replace(f"{{{key}}}", str(value))
                
            # Kommando ausführen
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=config.get('timeout', 60)
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': 'Command timeout'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _execute_script(self, config: Dict, context: Dict) -> Dict:
        """Führt Skript aus"""
        try:
            script_path = Path(config['script_path'])
            
            if not script_path.exists():
                return {'success': False, 'error': f'Script not found: {script_path}'}
                
            # Skript-Typ bestimmen
            if script_path.suffix.lower() == '.py':
                command = f'python "{script_path}"'
            elif script_path.suffix.lower() == '.ps1':
                command = f'powershell -ExecutionPolicy Bypass -File "{script_path}"'
            elif script_path.suffix.lower() in ['.bat', '.cmd']:
                command = f'"{script_path}"'
            else:
                command = f'"{script_path}"'
                
            # Argumente hinzufügen
            args = config.get('arguments', [])
            for arg in args:
                # Template-Variablen in Argumenten ersetzen
                for key, value in context.items():
                    arg = arg.replace(f"{{{key}}}", str(value))
                command += f' "{arg}"'
                
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=config.get('timeout', 300)
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _execute_function(self, config: Dict, context: Dict) -> Dict:
        """Führt Python-Funktion aus"""
        try:
            function_name = config['function']
            module_name = config.get('module', '__main__')
            
            # Funktion importieren und ausführen
            if module_name != '__main__':
                module = __import__(module_name, fromlist=[function_name])
                func = getattr(module, function_name)
            else:
                # Lokale Funktion
                func = globals().get(function_name)
                
            if not func:
                return {'success': False, 'error': f'Function not found: {function_name}'}
                
            # Funktion mit Kontext aufrufen
            result = func(context)
            
            return {'success': True, 'result': result}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def _send_notification(self, config: Dict, context: Dict) -> Dict:
        """Sendet Benachrichtigung"""
        try:
            title = config.get('title', 'Toobix Automation')
            message = config['message']
            
            # Template-Variablen in Nachricht ersetzen
            for key, value in context.items():
                message = message.replace(f"{{{key}}}", str(value))
                title = title.replace(f"{{{key}}}", str(value))
                
            # Windows-Benachrichtigung senden
            try:
                import win10toast
                toaster = win10toast.ToastNotifier()
                toaster.show_toast(title, message, duration=config.get('duration', 10))
            except ImportError:
                # Fallback: Console-Output
                print(f"NOTIFICATION: {title} - {message}")
                
            return {'success': True, 'title': title, 'message': message}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
            
    def get_automation_dashboard(self) -> Dict:
        """Erstellt Automatisierungs-Dashboard"""
        total_rules = len(self.automation_rules)
        enabled_rules = sum(1 for rule in self.automation_rules.values() if rule.enabled)
        total_executions = sum(rule.execution_count for rule in self.automation_rules.values())
        total_successes = sum(rule.success_count for rule in self.automation_rules.values())
        
        # Kürzlich ausgeführte Regeln
        recent_executions = []
        for rule in self.automation_rules.values():
            if rule.last_executed:
                recent_executions.append({
                    'name': rule.name,
                    'last_executed': rule.last_executed,
                    'success_rate': (rule.success_count / rule.execution_count * 100) if rule.execution_count > 0 else 0
                })
                
        recent_executions.sort(key=lambda x: x['last_executed'], reverse=True)
        
        return {
            'summary': {
                'total_rules': total_rules,
                'enabled_rules': enabled_rules,
                'total_executions': total_executions,
                'success_rate': (total_successes / total_executions * 100) if total_executions > 0 else 0
            },
            'recent_executions': recent_executions[:10],
            'trigger_types': {
                trigger_type.value: sum(1 for rule in self.automation_rules.values() 
                                       if rule.trigger_type == trigger_type)
                for trigger_type in TriggerType
            },
            'active_jobs': len(schedule.jobs),
            'file_watchers': len(self.file_watchers),
            'system_monitors': len(self.system_monitors)
        }
        
    def save_automation_rules(self) -> None:
        """Speichert Automatisierungs-Regeln"""
        try:
            rules_data = {}
            for rule_id, rule in self.automation_rules.items():
                rules_data[rule_id] = asdict(rule)
                # Enum-Werte in Strings konvertieren
                rules_data[rule_id]['trigger_type'] = rule.trigger_type.value
                rules_data[rule_id]['action_type'] = rule.action_type.value
                
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(rules_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Fehler beim Speichern der Automatisierungs-Regeln: {e}")
            
    def load_automation_rules(self) -> None:
        """Lädt gespeicherte Automatisierungs-Regeln"""
        try:
            if not self.config_file.exists():
                return
                
            with open(self.config_file, 'r', encoding='utf-8') as f:
                rules_data = json.load(f)
                
            for rule_id, rule_data in rules_data.items():
                rule = AutomationRule(
                    id=rule_data['id'],
                    name=rule_data['name'],
                    description=rule_data['description'],
                    trigger_type=TriggerType(rule_data['trigger_type']),
                    trigger_config=rule_data['trigger_config'],
                    action_type=ActionType(rule_data['action_type']),
                    action_config=rule_data['action_config'],
                    enabled=rule_data.get('enabled', True),
                    created_at=rule_data.get('created_at'),
                    last_executed=rule_data.get('last_executed'),
                    execution_count=rule_data.get('execution_count', 0),
                    success_count=rule_data.get('success_count', 0),
                    error_count=rule_data.get('error_count', 0)
                )
                
                self.automation_rules[rule_id] = rule
                
                # Trigger einrichten wenn enabled
                if rule.enabled:
                    self._setup_rule_trigger(rule)
                    
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Automatisierungs-Regeln: {e}")
            
    def create_quick_automations(self) -> List[Dict]:
        """Erstellt vordefinierte Quick-Automations"""
        quick_automations = [
            {
                'name': 'Tägliches Backup',
                'description': 'Erstellt täglich um 2:00 Uhr ein Backup wichtiger Dateien',
                'trigger_type': 'time',
                'trigger_config': {'time': '02:00'},
                'action_type': 'command',
                'action_config': {
                    'command': 'robocopy "C:\\Users\\%USERNAME%\\Documents" "C:\\Backup\\Documents" /MIR /LOG:backup.log'
                }
            },
            {
                'name': 'RAM-Warnung',
                'description': 'Benachrichtigung bei hohem RAM-Verbrauch',
                'trigger_type': 'system_event',
                'trigger_config': {'event_type': 'memory_high', 'threshold': 90},
                'action_type': 'notification',
                'action_config': {
                    'title': 'RAM-Warnung',
                    'message': 'Speicherverbrauch kritisch: {memory_percent}%'
                }
            },
            {
                'name': 'Downloads aufräumen',
                'description': 'Sortiert neue Downloads automatisch',
                'trigger_type': 'file_change',
                'trigger_config': {
                    'path': str(Path.home() / 'Downloads'),
                    'pattern': '*'
                },
                'action_type': 'function',
                'action_config': {
                    'function': 'organize_download',
                    'module': 'toobix.automation.file_organizer'
                }
            }
        ]
        
        return quick_automations
