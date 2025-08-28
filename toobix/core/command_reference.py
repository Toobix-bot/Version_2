"""
Toobix Command Reference System
Zeigt alle verfügbaren Befehle und ihre Funktionen
"""

class ToobixCommands:
    """Vollständige Referenz aller Toobix-Befehle"""
    
    def __init__(self):
        self.commands = self._initialize_commands()
    
    def _initialize_commands(self):
        """Initialisiert alle verfügbaren Befehle"""
        return {
            'system': {
                'title': '🖥️ SYSTEM-BEFEHLE',
                'commands': {
                    'analysiere system': {
                        'description': 'Analysiert System-Sauberkeit und findet Probleme',
                        'example': 'analysiere system',
                        'aliases': ['system analyse', 'system prüfen']
                    },
                    'aufräumplan': {
                        'description': 'Erstellt detaillierten Plan für System-Aufräumung',
                        'example': 'aufräumplan',
                        'aliases': ['aufräumen plan', 'cleanup plan']
                    },
                    'backup erstellen': {
                        'description': 'Erstellt Backup wichtiger Systemdateien',
                        'example': 'backup erstellen',
                        'aliases': ['sicherung', 'backup']
                    },
                    'aufräumen starten': {
                        'description': 'Führt System-Aufräumung durch (sichere Löschung)',
                        'example': 'aufräumen starten bestätigt',
                        'aliases': ['cleanup', 'aufräumen'],
                        'note': 'Verwende "bestätigt" für automatische Ausführung'
                    }
                }
            },
            'programs': {
                'title': '🚀 PROGRAMM-STEUERUNG', 
                'commands': {
                    'öffne [programm]': {
                        'description': 'Öffnet Programme oder Anwendungen',
                        'example': 'öffne notepad',
                        'supported': ['notepad', 'calculator', 'cmd', 'browser', 'explorer', 'vscode']
                    },
                    'finde datei [name]': {
                        'description': 'Sucht Dateien auf dem System',
                        'example': 'finde datei document.pdf'
                    }
                }
            },
            'projects': {
                'title': '📁 PROJEKT-MANAGEMENT',
                'commands': {
                    'scanne projekte': {
                        'description': 'Findet alle Code-Projekte in Standard-Verzeichnissen',
                        'example': 'scanne projekte',
                        'aliases': ['finde projekte', 'projekt scan']
                    },
                    'organisiere projekte': {
                        'description': 'Erstellt Plan zur besseren Projekt-Organisation',
                        'example': 'organisiere projekte',
                        'aliases': ['projekt organisation', 'ordne projekte']
                    },
                    'finde duplikate': {
                        'description': 'Findet doppelte oder ähnliche Projekte',
                        'example': 'finde duplikate',
                        'aliases': ['doppelte projekte', 'duplicates']
                    }
                }
            },
            'knowledge': {
                'title': '🧠 WISSENSBASIS',
                'commands': {
                    'merke dir [info]': {
                        'description': 'Speichert Information dauerhaft',
                        'example': 'merke dir mein API-Key als xyz123 - für Groq',
                        'pattern': 'merke dir [inhalt] als [wert] - [notiz]'
                    },
                    'was weißt du über [thema]': {
                        'description': 'Ruft gespeicherte Informationen ab',
                        'example': 'was weißt du über API-Key',
                        'aliases': ['erinnerst du dich an', 'was hast du über']
                    },
                    'zeige erinnerungen': {
                        'description': 'Zeigt komplette Wissensbasis-Zusammenfassung',
                        'example': 'zeige erinnerungen',
                        'aliases': ['was weißt du', 'memory summary']
                    },
                    'vorschläge': {
                        'description': 'Zeigt personalisierte Empfehlungen basierend auf Gewohnheiten',
                        'example': 'vorschläge',
                        'aliases': ['empfehlungen', 'was soll ich']
                    }
                }
            },
            'speech': {
                'title': '🎤 SPRACH-STEUERUNG',
                'commands': {
                    'F1-Taste': {
                        'description': 'Aktiviert einmalige Spracheingabe',
                        'example': 'Drücke F1, dann sprich deinen Befehl'
                    },
                    'hey toobix': {
                        'description': 'Wake-Word für kontinuierliche Spracherkennung',
                        'example': 'Sage "Hey Toobix" gefolgt von deinem Befehl',
                        'note': 'Automatische Aktivierung alle 30 Sekunden'
                    }
                }
            },
            'ai': {
                'title': '🤖 KI-INTERAKTION',
                'commands': {
                    'normale chat-befehle': {
                        'description': 'Stelle beliebige Fragen oder bitte um Hilfe',
                        'example': 'Wie kann ich Python lernen?',
                        'note': 'Verwendet intelligente Weiterleitung zwischen lokaler und Cloud-KI'
                    },
                    'ai status': {
                        'description': 'Zeigt Status von lokaler (Ollama) und Cloud-KI (Groq)',
                        'example': 'Klicke AI Status Button'
                    }
                }
            },
            'automation': {
                'title': '⚙️ AUTOMATISIERUNG',
                'commands': {
                    'automatisierung vorschläge': {
                        'description': 'Schlägt Automatisierungen basierend auf Nutzungsmustern vor',
                        'example': 'automatisierung vorschläge',
                        'note': 'Wird automatisch nach ausreichender Nutzung angeboten'
                    }
                }
            },
            'shortcuts': {
                'title': '⌨️ TASTATUR-SHORTCUTS',
                'commands': {
                    'Enter': {
                        'description': 'Sendet Nachricht'
                    },
                    'F1': {
                        'description': 'Aktiviert Spracheingabe'
                    },
                    'ESC': {
                        'description': 'Fokus zurück auf Eingabefeld'
                    }
                }
            }
        }
    
    def get_command_list(self, category=None):
        """Gibt Befehlsliste zurück"""
        if category and category in self.commands:
            return self._format_category(category, self.commands[category])
        
        # Alle Kategorien
        result = "📚 TOOBIX BEFEHLSREFERENZ\n"
        result += "=" * 50 + "\n\n"
        
        for cat_name, cat_data in self.commands.items():
            result += self._format_category(cat_name, cat_data) + "\n"
        
        result += "\n💡 TIPPS:\n"
        result += "• Befehle sind nicht case-sensitive\n"
        result += "• Verwende natürliche Sprache\n"
        result += "• Bei Problemen: 'hilfe [kategorie]' für Details\n"
        result += "• Toobix lernt deine Gewohnheiten für bessere Vorschläge\n"
        
        return result
    
    def _format_category(self, cat_name, cat_data):
        """Formatiert eine Befehls-Kategorie"""
        result = f"{cat_data['title']}\n"
        result += "-" * len(cat_data['title']) + "\n"
        
        for cmd, details in cat_data['commands'].items():
            result += f"• {cmd}\n"
            result += f"  {details['description']}\n"
            
            if 'example' in details:
                result += f"  Beispiel: {details['example']}\n"
            
            if 'aliases' in details:
                result += f"  Auch: {', '.join(details['aliases'])}\n"
            
            if 'supported' in details:
                result += f"  Unterstützt: {', '.join(details['supported'])}\n"
            
            if 'pattern' in details:
                result += f"  Muster: {details['pattern']}\n"
            
            if 'note' in details:
                result += f"  Hinweis: {details['note']}\n"
            
            result += "\n"
        
        return result
    
    def search_commands(self, query):
        """Sucht Befehle nach Stichwort"""
        query = query.lower()
        results = []
        
        for cat_name, cat_data in self.commands.items():
            for cmd, details in cat_data['commands'].items():
                # Suche in Command-Name
                if query in cmd.lower():
                    results.append((cat_name, cmd, details))
                # Suche in Beschreibung
                elif query in details['description'].lower():
                    results.append((cat_name, cmd, details))
                # Suche in Aliases
                elif 'aliases' in details:
                    for alias in details['aliases']:
                        if query in alias.lower():
                            results.append((cat_name, cmd, details))
                            break
        
        if not results:
            return f"❌ Keine Befehle gefunden für '{query}'"
        
        result = f"🔍 SUCHERGEBNISSE FÜR '{query}':\n\n"
        for cat, cmd, details in results:
            result += f"• {cmd} ({self.commands[cat]['title']})\n"
            result += f"  {details['description']}\n\n"
        
        return result
    
    def get_category_help(self, category):
        """Gibt detaillierte Hilfe für eine Kategorie"""
        if category not in self.commands:
            available = ', '.join(self.commands.keys())
            return f"❌ Kategorie '{category}' nicht gefunden.\nVerfügbar: {available}"
        
        return self._format_category(category, self.commands[category])
    
    def get_quick_help(self):
        """Gibt schnelle Übersicht der wichtigsten Befehle"""
        quick_commands = [
            ('analysiere system', 'Prüft System-Gesundheit'),
            ('scanne projekte', 'Findet Code-Projekte'),  
            ('merke dir [info]', 'Speichert Informationen'),
            ('öffne [programm]', 'Startet Programme'),
            ('vorschläge', 'Personalisierte Empfehlungen'),
            ('hilfe', 'Zeigt alle Befehle')
        ]
        
        result = "⚡ WICHTIGSTE BEFEHLE:\n\n"
        for cmd, desc in quick_commands:
            result += f"• {cmd} - {desc}\n"
        
        result += "\n💬 Oder stelle einfach eine Frage!"
        return result
