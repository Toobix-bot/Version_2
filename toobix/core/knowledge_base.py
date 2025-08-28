"""
Toobix Knowledge Base & Memory System
Lernt über das System und den Benutzer, merkt sich Präferenzen und Gewohnheiten
"""
import json
import os
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class KnowledgeBase:
    """Intelligentes Wissens- und Erinnerungssystem für Toobix"""
    
    def __init__(self, settings):
        self.settings = settings
        self.knowledge_file = Path(os.path.expanduser("~/.toobix_knowledge.json"))
        self.interaction_log = Path(os.path.expanduser("~/.toobix_interactions.json"))
        
        # Lade existierendes Wissen
        self.knowledge = self._load_knowledge()
        self.interactions = self._load_interactions()
        
        print("🧠 Knowledge Base initialisiert")
    
    def _load_knowledge(self) -> Dict:
        """Lädt gespeichertes Wissen"""
        default_knowledge = {
            'user_profile': {
                'name': None,
                'preferred_language': 'de',
                'programming_languages': [],
                'favorite_tools': [],
                'work_schedule': {},
                'project_preferences': {}
            },
            'system_profile': {
                'os': 'Windows',
                'installed_programs': [],
                'common_directories': [],
                'project_locations': [],
                'file_patterns': {}
            },
            'learned_behaviors': {
                'frequently_used_commands': {},
                'common_file_types': {},
                'preferred_organization': {},
                'automation_opportunities': []
            },
            'project_memory': {
                'known_projects': {},
                'project_relationships': {},
                'code_patterns': {},
                'technology_stacks': []
            },
            'personal_notes': {},
            'automation_rules': [],
            'last_updated': time.time()
        }
        
        if self.knowledge_file.exists():
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    stored = json.load(f)
                    # Merge mit default structure
                    for key in default_knowledge:
                        if key not in stored:
                            stored[key] = default_knowledge[key]
                    return stored
            except Exception as e:
                print(f"⚠️ Fehler beim Laden des Wissens: {e}")
        
        return default_knowledge
    
    def _load_interactions(self) -> List[Dict]:
        """Lädt Interaktions-Historie"""
        if self.interaction_log.exists():
            try:
                with open(self.interaction_log, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Fehler beim Laden der Interaktionen: {e}")
        return []
    
    def save_knowledge(self):
        """Speichert aktuelles Wissen"""
        try:
            self.knowledge['last_updated'] = time.time()
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                json.dump(self.knowledge, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern des Wissens: {e}")
    
    def log_interaction(self, command: str, response: str, context: Dict = None):
        """Loggt eine Benutzer-Interaktion"""
        interaction = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'command': command,
            'response_type': self._classify_response(response),
            'context': context or {},
            'success': not response.startswith('❌')
        }
        
        self.interactions.append(interaction)
        
        # Begrenzt Historie auf 1000 Einträge
        if len(self.interactions) > 1000:
            self.interactions = self.interactions[-1000:]
        
        # Lerne aus der Interaktion
        self._learn_from_interaction(interaction)
        
        # Speichere periodisch
        if len(self.interactions) % 10 == 0:
            self._save_interactions()
    
    def _save_interactions(self):
        """Speichert Interaktions-Log"""
        try:
            with open(self.interaction_log, 'w', encoding='utf-8') as f:
                json.dump(self.interactions, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Fehler beim Speichern der Interaktionen: {e}")
    
    def _classify_response(self, response: str) -> str:
        """Klassifiziert den Typ der Antwort"""
        if '✅' in response or 'erfolgreich' in response.lower():
            return 'success_action'
        elif '🔍' in response or 'gefunden' in response.lower():
            return 'search_result'
        elif '🧹' in response or 'aufräum' in response.lower():
            return 'cleanup_action'
        elif '💾' in response or 'backup' in response.lower():
            return 'backup_action'
        elif '❌' in response or 'fehler' in response.lower():
            return 'error'
        elif '🤖' in response:
            return 'ai_response'
        else:
            return 'general'
    
    def _learn_from_interaction(self, interaction: Dict):
        """Lernt aus einer Benutzer-Interaktion"""
        command = interaction['command'].lower()
        
        # Häufig verwendete Befehle
        if command not in self.knowledge['learned_behaviors']['frequently_used_commands']:
            self.knowledge['learned_behaviors']['frequently_used_commands'][command] = 0
        self.knowledge['learned_behaviors']['frequently_used_commands'][command] += 1
        
        # Programmiersprachen erkennen
        for lang in ['python', 'javascript', 'java', 'c++', 'c#', 'php', 'go', 'rust']:
            if lang in command:
                if lang not in self.knowledge['user_profile']['programming_languages']:
                    self.knowledge['user_profile']['programming_languages'].append(lang)
        
        # Tools und Programme
        programs = ['vscode', 'notepad', 'browser', 'excel', 'word', 'calculator']
        for program in programs:
            if program in command and 'öffne' in command:
                if program not in self.knowledge['user_profile']['favorite_tools']:
                    self.knowledge['user_profile']['favorite_tools'].append(program)
        
        # Projekt-bezogene Aktivitäten
        if any(word in command for word in ['projekt', 'code', 'entwickl', 'programm']):
            self._learn_project_pattern(command, interaction)
        
        # Zeitbasierte Muster
        hour = datetime.now().hour
        if hour not in self.knowledge['user_profile']['work_schedule']:
            self.knowledge['user_profile']['work_schedule'][str(hour)] = 0
        self.knowledge['user_profile']['work_schedule'][str(hour)] += 1
    
    def _learn_project_pattern(self, command: str, interaction: Dict):
        """Lernt Projekt-bezogene Muster"""
        context = interaction.get('context', {})
        
        # Projekt-Verzeichnisse
        if 'path' in context:
            path = context['path']
            if any(indicator in path.lower() for indicator in ['project', 'code', 'dev']):
                if path not in self.knowledge['system_profile']['project_locations']:
                    self.knowledge['system_profile']['project_locations'].append(path)
    
    def get_personalized_suggestions(self) -> List[str]:
        """Gibt personalisierte Vorschläge basierend auf gelerntem Verhalten"""
        suggestions = []
        
        # Häufige Befehle
        frequent_commands = sorted(
            self.knowledge['learned_behaviors']['frequently_used_commands'].items(),
            key=lambda x: x[1], reverse=True
        )[:3]
        
        if frequent_commands:
            suggestions.append(f"💡 Deine häufigsten Befehle: {', '.join([cmd[0] for cmd in frequent_commands])}")
        
        # Arbeitszeit-Muster
        current_hour = datetime.now().hour
        work_schedule = self.knowledge['user_profile']['work_schedule']
        if work_schedule and str(current_hour) in work_schedule:
            if work_schedule[str(current_hour)] > 5:  # Mindestens 5 Interaktionen zu dieser Zeit
                suggestions.append(f"⏰ Du arbeitest oft um diese Zeit - soll ich dein übliches Setup vorbereiten?")
        
        # Projekt-Vorschläge
        if self.knowledge['user_profile']['programming_languages']:
            langs = ', '.join(self.knowledge['user_profile']['programming_languages'])
            suggestions.append(f"🔧 Erkannte Programmiersprachen: {langs}")
        
        # Aufräum-Erinnerungen
        days_since_cleanup = (time.time() - self.knowledge.get('last_cleanup', 0)) / (24 * 3600)
        if days_since_cleanup > 7:
            suggestions.append("🧹 Es ist eine Woche her seit der letzten Aufräumung - Zeit für System-Check?")
        
        return suggestions
    
    def remember_fact(self, category: str, key: str, value: Any, note: str = None):
        """Merkt sich einen spezifischen Fakt"""
        if category not in self.knowledge['personal_notes']:
            self.knowledge['personal_notes'][category] = {}
        
        self.knowledge['personal_notes'][category][key] = {
            'value': value,
            'note': note,
            'learned_at': time.time(),
            'datetime': datetime.now().isoformat()
        }
        
        self.save_knowledge()
        return f"✅ Gemerkt: {key} = {value}" + (f" ({note})" if note else "")
    
    def recall_fact(self, category: str, key: str = None) -> str:
        """Ruft gespeicherte Fakten ab"""
        if category not in self.knowledge['personal_notes']:
            return f"❌ Keine Informationen zu '{category}' gespeichert"
        
        if key:
            if key in self.knowledge['personal_notes'][category]:
                fact = self.knowledge['personal_notes'][category][key]
                learned_date = datetime.fromtimestamp(fact['learned_at']).strftime('%d.%m.%Y')
                return f"💭 {key}: {fact['value']}" + (f" ({fact['note']})" if fact['note'] else "") + f" [gespeichert: {learned_date}]"
            else:
                return f"❌ '{key}' in Kategorie '{category}' nicht gefunden"
        else:
            # Alle Fakten der Kategorie
            facts = self.knowledge['personal_notes'][category]
            if not facts:
                return f"❌ Kategorie '{category}' ist leer"
            
            result = f"💭 Gespeicherte Informationen zu '{category}':\n"
            for k, v in facts.items():
                result += f"• {k}: {v['value']}\n"
            return result
    
    def get_memory_summary(self) -> str:
        """Gibt Zusammenfassung des gespeicherten Wissens"""
        total_interactions = len(self.interactions)
        days_active = (time.time() - self.knowledge.get('first_interaction', time.time())) / (24 * 3600)
        
        summary = f"🧠 TOOBIX ERINNERUNGS-BERICHT\n\n"
        summary += f"📊 Aktivität: {total_interactions} Interaktionen über {int(days_active)} Tage\n\n"
        
        # Benutzer-Profil
        user = self.knowledge['user_profile']
        summary += f"👤 BENUTZER-PROFIL:\n"
        if user['programming_languages']:
            summary += f"• Programmiersprachen: {', '.join(user['programming_languages'])}\n"
        if user['favorite_tools']:
            summary += f"• Lieblings-Tools: {', '.join(user['favorite_tools'])}\n"
        
        # Häufige Befehle
        frequent = self.knowledge['learned_behaviors']['frequently_used_commands']
        if frequent:
            top_commands = sorted(frequent.items(), key=lambda x: x[1], reverse=True)[:5]
            summary += f"\n🔄 HÄUFIGSTE BEFEHLE:\n"
            for cmd, count in top_commands:
                summary += f"• {cmd}: {count}x\n"
        
        # Projekt-Informationen
        projects = self.knowledge['system_profile']['project_locations']
        if projects:
            summary += f"\n📁 BEKANNTE PROJEKT-VERZEICHNISSE:\n"
            for project in projects[:5]:
                summary += f"• {project}\n"
        
        # Persönliche Notizen
        notes = self.knowledge['personal_notes']
        if notes:
            summary += f"\n📝 GESPEICHERTE KATEGORIEN:\n"
            for category, items in notes.items():
                summary += f"• {category}: {len(items)} Einträge\n"
        
        return summary
    
    def suggest_automation(self) -> List[Dict]:
        """Schlägt Automatisierung basierend auf Mustern vor"""
        automations = []
        
        # Häufige Befehls-Ketten
        frequent = self.knowledge['learned_behaviors']['frequently_used_commands']
        
        # Tägliche Aufräum-Routine
        if frequent.get('analysiere system', 0) > 3:
            automations.append({
                'type': 'daily_cleanup_check',
                'title': 'Täglicher System-Check',
                'description': 'Automatische System-Analyse jeden Morgen um 9:00',
                'command': 'analysiere system',
                'schedule': 'daily_9am'
            })
        
        # Projekt-Backup
        if frequent.get('backup', 0) > 2:
            automations.append({
                'type': 'project_backup',
                'title': 'Wöchentliches Projekt-Backup',
                'description': 'Automatisches Backup aller Projekte jeden Freitag',
                'command': 'erstelle backup',
                'schedule': 'weekly_friday'
            })
        
        # Arbeitszeit-Setup
        work_hours = self.knowledge['user_profile']['work_schedule']
        if work_hours:
            peak_hour = max(work_hours.items(), key=lambda x: x[1])[0]
            automations.append({
                'type': 'workday_setup',
                'title': f'Arbeitsplatz-Setup um {peak_hour}:00',
                'description': f'Öffne häufig verwendete Tools automatisch um {peak_hour}:00',
                'command': 'setup workspace',
                'schedule': f'daily_{peak_hour}am'
            })
        
        return automations
    
    def create_user_context(self) -> str:
        """Erstellt persönlichen Kontext für AI-Antworten"""
        context = []
        
        # Name falls bekannt
        if self.knowledge['user_profile']['name']:
            context.append(f"Benutzer: {self.knowledge['user_profile']['name']}")
        
        # Programmiersprachen
        langs = self.knowledge['user_profile']['programming_languages']
        if langs:
            context.append(f"Programmiert in: {', '.join(langs)}")
        
        # Aktuelle Tageszeit-Aktivität
        current_hour = datetime.now().hour
        work_schedule = self.knowledge['user_profile']['work_schedule']
        if str(current_hour) in work_schedule and work_schedule[str(current_hour)] > 3:
            context.append(f"Arbeitet oft um diese Zeit ({current_hour}:00)")
        
        # Häufige Aktivitäten
        frequent = self.knowledge['learned_behaviors']['frequently_used_commands']
        if frequent:
            top_activity = max(frequent.items(), key=lambda x: x[1])[0]
            context.append(f"Häufigste Aktivität: {top_activity}")
        
        return " | ".join(context) if context else "Neuer Benutzer"
