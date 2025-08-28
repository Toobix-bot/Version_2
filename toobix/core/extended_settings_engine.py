"""
Toobix Extended Settings & Interface Engine
Erweiterte Einstellungen und Interface-Optionen für vollständige Systemkontrolle
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict, field
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SettingOption:
    """Einzelne Einstellungs-Option"""
    key: str
    display_name: str
    description: str
    value_type: str  # bool, int, float, string, list, dict
    default_value: Any
    current_value: Any
    category: str
    subcategory: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    options: Optional[List[str]] = None
    requires_restart: bool = False
    advanced: bool = False
    tooltip: Optional[str] = None

@dataclass
class InterfaceTheme:
    """Interface-Theme Definition"""
    name: str
    display_name: str
    colors: Dict[str, str]
    fonts: Dict[str, str]
    spacing: Dict[str, int]
    animations: Dict[str, bool]
    custom_css: Optional[str] = None

@dataclass
class LayoutConfiguration:
    """Layout-Konfiguration"""
    name: str
    display_name: str
    panels: List[str]
    panel_positions: Dict[str, Dict[str, Any]]
    default_sizes: Dict[str, Dict[str, int]]
    responsive_breakpoints: Dict[str, int] = field(default_factory=dict)

class ExtendedSettingsEngine:
    """
    Extended Settings Engine für vollständige Systemkonfiguration
    """
    
    def __init__(self):
        """Initialisiert Extended Settings Engine"""
        self.settings_file = Path('toobix_settings.json')
        self.themes_file = Path('toobix_themes.json')
        self.layouts_file = Path('toobix_layouts.json')
        
        # Aktuelle Einstellungen
        self.settings = {}
        self.themes = {}
        self.layouts = {}
        self.current_theme = "default"
        self.current_layout = "default"
        
        # Change Callbacks
        self.change_callbacks = []
        
        # Initialisiere Standard-Einstellungen
        self._initialize_default_settings()
        self._initialize_default_themes()
        self._initialize_default_layouts()
        
        # Lade existierende Einstellungen
        self._load_settings()
        
        logger.info("⚙️ Extended Settings Engine initialisiert")
    
    def _initialize_default_settings(self) -> None:
        """Initialisiert Standard-Einstellungen"""
        self.default_settings = {
            # === AI & INTELLIGENZ ===
            'ai_model_primary': SettingOption(
                key='ai_model_primary',
                display_name='Primäres AI Modell',
                description='Hauptmodell für AI-Verarbeitung',
                value_type='string',
                default_value='gemma2:2b',
                current_value='gemma2:2b',
                category='AI & Intelligenz',
                options=['gemma2:2b', 'llama2', 'mistral', 'codellama'],
                tooltip='Wähle das Hauptmodell für AI-Operationen'
            ),
            'ai_model_fallback': SettingOption(
                key='ai_model_fallback',
                display_name='Fallback AI Modell',
                description='Backup-Modell bei Problemen',
                value_type='string',
                default_value='groq-cloud',
                current_value='groq-cloud',
                category='AI & Intelligenz',
                options=['groq-cloud', 'openai-api', 'local-backup'],
                tooltip='Fallback wenn primäres Modell nicht verfügbar'
            ),
            'ai_response_temperature': SettingOption(
                key='ai_response_temperature',
                display_name='AI Kreativitäts-Level',
                description='Steuert Kreativität der AI-Antworten',
                value_type='float',
                default_value=0.7,
                current_value=0.7,
                category='AI & Intelligenz',
                min_value=0.0,
                max_value=2.0,
                tooltip='0.0 = sehr konsistent, 2.0 = sehr kreativ'
            ),
            'ai_max_tokens': SettingOption(
                key='ai_max_tokens',
                display_name='Maximale Response-Länge',
                description='Maximum Tokens für AI-Antworten',
                value_type='int',
                default_value=2048,
                current_value=2048,
                category='AI & Intelligenz',
                min_value=128,
                max_value=8192,
                tooltip='Höhere Werte = längere Antworten'
            ),
            'ai_context_memory': SettingOption(
                key='ai_context_memory',
                display_name='Kontext-Gedächtnis',
                description='Anzahl gespeicherter Konversations-Nachrichten',
                value_type='int',
                default_value=20,
                current_value=20,
                category='AI & Intelligenz',
                min_value=5,
                max_value=100,
                tooltip='Mehr Kontext = bessere Kontinuität'
            ),
            
            # === SPRACH-STEUERUNG ===
            'speech_recognition_enabled': SettingOption(
                key='speech_recognition_enabled',
                display_name='Spracherkennung aktiv',
                description='Aktiviert Sprach-zu-Text Funktion',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Sprach-Steuerung'
            ),
            'speech_synthesis_enabled': SettingOption(
                key='speech_synthesis_enabled',
                display_name='Sprachausgabe aktiv',
                description='Aktiviert Text-zu-Sprache Ausgabe',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Sprach-Steuerung'
            ),
            'speech_recognition_language': SettingOption(
                key='speech_recognition_language',
                display_name='Sprache für Erkennung',
                description='Sprache für Spracherkennung',
                value_type='string',
                default_value='de-DE',
                current_value='de-DE',
                category='Sprach-Steuerung',
                options=['de-DE', 'en-US', 'en-GB', 'fr-FR', 'es-ES'],
                tooltip='Unterstützte Sprachen für Spracherkennung'
            ),
            'speech_voice_type': SettingOption(
                key='speech_voice_type',
                display_name='Stimmen-Typ',
                description='Typ der Sprachausgabe-Stimme',
                value_type='string',
                default_value='female',
                current_value='female',
                category='Sprach-Steuerung',
                options=['male', 'female', 'neutral'],
                tooltip='Wähle den bevorzugten Stimmen-Typ'
            ),
            'speech_rate': SettingOption(
                key='speech_rate',
                display_name='Sprach-Geschwindigkeit',
                description='Geschwindigkeit der Sprachausgabe',
                value_type='float',
                default_value=1.0,
                current_value=1.0,
                category='Sprach-Steuerung',
                min_value=0.5,
                max_value=2.0,
                tooltip='1.0 = normale Geschwindigkeit'
            ),
            'wake_word_enabled': SettingOption(
                key='wake_word_enabled',
                display_name='Wake Word aktiv',
                description='Aktiviert Wake Word für Sprachaktivierung',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Sprach-Steuerung'
            ),
            'wake_word': SettingOption(
                key='wake_word',
                display_name='Wake Word',
                description='Wort zum Aktivieren der Spracherkennung',
                value_type='string',
                default_value='Toobix',
                current_value='Toobix',
                category='Sprach-Steuerung',
                tooltip='Sage dieses Wort um Toobix zu aktivieren'
            ),
            
            # === PRODUKTIVITÄT ===
            'productivity_tracking_enabled': SettingOption(
                key='productivity_tracking_enabled',
                display_name='Produktivitäts-Tracking',
                description='Aktiviert automatisches Produktivitäts-Tracking',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Produktivität'
            ),
            'focus_mode_enabled': SettingOption(
                key='focus_mode_enabled',
                display_name='Focus Mode verfügbar',
                description='Aktiviert Focus Mode Funktionalität',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Produktivität'
            ),
            'pomodoro_duration': SettingOption(
                key='pomodoro_duration',
                display_name='Pomodoro Dauer (Minuten)',
                description='Dauer einer Pomodoro Session',
                value_type='int',
                default_value=25,
                current_value=25,
                category='Produktivität',
                min_value=15,
                max_value=60,
                tooltip='Standard: 25 Minuten pro Session'
            ),
            'break_duration': SettingOption(
                key='break_duration',
                display_name='Pausen-Dauer (Minuten)',
                description='Dauer der Pausen zwischen Sessions',
                value_type='int',
                default_value=5,
                current_value=5,
                category='Produktivität',
                min_value=3,
                max_value=15,
                tooltip='Standard: 5 Minuten Pause'
            ),
            'daily_goal_hours': SettingOption(
                key='daily_goal_hours',
                display_name='Tägliches Stunden-Ziel',
                description='Ziel-Arbeitszeit pro Tag',
                value_type='float',
                default_value=8.0,
                current_value=8.0,
                category='Produktivität',
                min_value=1.0,
                max_value=16.0,
                tooltip='Produktive Stunden als Tagesziel'
            ),
            
            # === SYSTEM & PERFORMANCE ===
            'auto_optimization_enabled': SettingOption(
                key='auto_optimization_enabled',
                display_name='Auto-Optimierung',
                description='Automatische System-Optimierung',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='System & Performance'
            ),
            'memory_cleanup_interval': SettingOption(
                key='memory_cleanup_interval',
                display_name='Speicher-Bereinigung (Minuten)',
                description='Intervall für automatische Speicher-Bereinigung',
                value_type='int',
                default_value=30,
                current_value=30,
                category='System & Performance',
                min_value=10,
                max_value=120,
                tooltip='Häufigere Bereinigung = weniger RAM-Verbrauch'
            ),
            'cpu_usage_threshold': SettingOption(
                key='cpu_usage_threshold',
                display_name='CPU Warnschwelle (%)',
                description='CPU-Auslastung ab der gewarnt wird',
                value_type='float',
                default_value=80.0,
                current_value=80.0,
                category='System & Performance',
                min_value=50.0,
                max_value=95.0,
                tooltip='Warnung bei hoher CPU-Last'
            ),
            'disk_cleanup_enabled': SettingOption(
                key='disk_cleanup_enabled',
                display_name='Festplatten-Bereinigung',
                description='Automatische Bereinigung temporärer Dateien',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='System & Performance'
            ),
            
            # === WELLNESS ===
            'wellness_tracking_enabled': SettingOption(
                key='wellness_tracking_enabled',
                display_name='Wellness Tracking',
                description='Aktiviert Wellness- und Gesundheits-Tracking',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Wellness'
            ),
            'break_reminders_enabled': SettingOption(
                key='break_reminders_enabled',
                display_name='Pausen-Erinnerungen',
                description='Automatische Erinnerungen für Pausen',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Wellness'
            ),
            'stress_monitoring_enabled': SettingOption(
                key='stress_monitoring_enabled',
                display_name='Stress Monitoring',
                description='Überwacht Stress-Level und gibt Empfehlungen',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Wellness'
            ),
            'meditation_reminders': SettingOption(
                key='meditation_reminders',
                display_name='Meditations-Erinnerungen',
                description='Regelmäßige Meditation-Vorschläge',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Wellness'
            ),
            'daily_wellness_goal': SettingOption(
                key='daily_wellness_goal',
                display_name='Tägliches Wellness-Ziel',
                description='Anzahl Wellness-Aktivitäten pro Tag',
                value_type='int',
                default_value=3,
                current_value=3,
                category='Wellness',
                min_value=1,
                max_value=10,
                tooltip='Meditationen, Pausen, Übungen etc.'
            ),
            
            # === INTERFACE & DESIGN ===
            'theme': SettingOption(
                key='theme',
                display_name='Design-Theme',
                description='Visuelles Design des Interface',
                value_type='string',
                default_value='default',
                current_value='default',
                category='Interface & Design',
                options=['default', 'dark', 'light', 'blue', 'green', 'purple', 'minimal'],
                tooltip='Wähle dein bevorzugtes Design'
            ),
            'layout': SettingOption(
                key='layout',
                display_name='Interface Layout',
                description='Anordnung der Interface-Elemente',
                value_type='string',
                default_value='default',
                current_value='default',
                category='Interface & Design',
                options=['default', 'compact', 'spacious', 'sidebar', 'tabs', 'floating'],
                tooltip='Verschiedene Layout-Optionen'
            ),
            'font_size': SettingOption(
                key='font_size',
                display_name='Schriftgröße',
                description='Größe der Interface-Schrift',
                value_type='int',
                default_value=12,
                current_value=12,
                category='Interface & Design',
                min_value=8,
                max_value=24,
                tooltip='Pixel-Größe der Schrift'
            ),
            'animations_enabled': SettingOption(
                key='animations_enabled',
                display_name='Animationen aktiv',
                description='Aktiviert Interface-Animationen',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Interface & Design'
            ),
            'transparency_level': SettingOption(
                key='transparency_level',
                display_name='Transparenz-Level',
                description='Transparenz des Interface',
                value_type='float',
                default_value=0.95,
                current_value=0.95,
                category='Interface & Design',
                min_value=0.5,
                max_value=1.0,
                tooltip='1.0 = vollständig undurchsichtig'
            ),
            
            # === GEDANKENSTROM ===
            'thought_stream_enabled': SettingOption(
                key='thought_stream_enabled',
                display_name='KI Gedankenstrom aktiv',
                description='Aktiviert kontinuierlichen KI-Gedankenstrom',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='KI Gedankenstrom'
            ),
            'thought_frequency': SettingOption(
                key='thought_frequency',
                display_name='Gedanken-Frequenz (Sekunden)',
                description='Intervall zwischen KI-Gedanken',
                value_type='int',
                default_value=45,
                current_value=45,
                category='KI Gedankenstrom',
                min_value=15,
                max_value=300,
                tooltip='Häufigere Gedanken = mehr Interaktion'
            ),
            'thought_creativity_level': SettingOption(
                key='thought_creativity_level',
                display_name='Kreativitäts-Level',
                description='Kreativität der KI-Gedanken',
                value_type='float',
                default_value=0.7,
                current_value=0.7,
                category='KI Gedankenstrom',
                min_value=0.0,
                max_value=1.0,
                tooltip='0.0 = praktisch, 1.0 = sehr kreativ'
            ),
            'auto_insights_enabled': SettingOption(
                key='auto_insights_enabled',
                display_name='Auto-Insights aktiv',
                description='Automatische Einsichten und Empfehlungen',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='KI Gedankenstrom'
            ),
            
            # === ERWEITERTE EINSTELLUNGEN ===
            'debug_mode_enabled': SettingOption(
                key='debug_mode_enabled',
                display_name='Debug-Modus',
                description='Aktiviert erweiterte Debug-Informationen',
                value_type='bool',
                default_value=False,
                current_value=False,
                category='Erweiterte Einstellungen',
                advanced=True,
                requires_restart=True
            ),
            'logging_level': SettingOption(
                key='logging_level',
                display_name='Logging-Level',
                description='Detailgrad der System-Logs',
                value_type='string',
                default_value='INFO',
                current_value='INFO',
                category='Erweiterte Einstellungen',
                options=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                advanced=True,
                requires_restart=True
            ),
            'auto_backup_enabled': SettingOption(
                key='auto_backup_enabled',
                display_name='Auto-Backup',
                description='Automatische Sicherung von Einstellungen',
                value_type='bool',
                default_value=True,
                current_value=True,
                category='Erweiterte Einstellungen',
                advanced=True
            ),
            'experimental_features_enabled': SettingOption(
                key='experimental_features_enabled',
                display_name='Experimentelle Features',
                description='Aktiviert experimentelle Funktionen',
                value_type='bool',
                default_value=False,
                current_value=False,
                category='Erweiterte Einstellungen',
                advanced=True,
                tooltip='Kann zu Instabilität führen'
            )
        }
    
    def _initialize_default_themes(self) -> None:
        """Initialisiert Standard-Themes"""
        self.default_themes = {
            'default': InterfaceTheme(
                name='default',
                display_name='Standard',
                colors={
                    'primary': '#3498db',
                    'secondary': '#2ecc71',
                    'background': '#ffffff',
                    'surface': '#f8f9fa',
                    'text': '#2c3e50',
                    'text_secondary': '#7f8c8d',
                    'accent': '#e74c3c',
                    'success': '#27ae60',
                    'warning': '#f39c12',
                    'error': '#e74c3c'
                },
                fonts={
                    'primary': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                    'secondary': 'Consolas, Monaco, monospace',
                    'heading': 'Arial, Helvetica, sans-serif'
                },
                spacing={
                    'xs': 4,
                    'sm': 8,
                    'md': 16,
                    'lg': 24,
                    'xl': 32
                },
                animations={
                    'fade_enabled': True,
                    'slide_enabled': True,
                    'scale_enabled': True
                }
            ),
            'dark': InterfaceTheme(
                name='dark',
                display_name='Dark Mode',
                colors={
                    'primary': '#61dafb',
                    'secondary': '#98fb98',
                    'background': '#1e1e1e',
                    'surface': '#2d2d2d',
                    'text': '#ffffff',
                    'text_secondary': '#b0b0b0',
                    'accent': '#ff6b6b',
                    'success': '#51cf66',
                    'warning': '#ffd43b',
                    'error': '#ff6b6b'
                },
                fonts={
                    'primary': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif',
                    'secondary': 'Consolas, Monaco, monospace',
                    'heading': 'Arial, Helvetica, sans-serif'
                },
                spacing={
                    'xs': 4,
                    'sm': 8,
                    'md': 16,
                    'lg': 24,
                    'xl': 32
                },
                animations={
                    'fade_enabled': True,
                    'slide_enabled': True,
                    'scale_enabled': True
                }
            ),
            'minimal': InterfaceTheme(
                name='minimal',
                display_name='Minimal',
                colors={
                    'primary': '#000000',
                    'secondary': '#666666',
                    'background': '#ffffff',
                    'surface': '#fafafa',
                    'text': '#333333',
                    'text_secondary': '#999999',
                    'accent': '#0066cc',
                    'success': '#00aa00',
                    'warning': '#ffaa00',
                    'error': '#cc0000'
                },
                fonts={
                    'primary': 'Arial, sans-serif',
                    'secondary': 'Courier New, monospace',
                    'heading': 'Helvetica, sans-serif'
                },
                spacing={
                    'xs': 2,
                    'sm': 4,
                    'md': 8,
                    'lg': 16,
                    'xl': 24
                },
                animations={
                    'fade_enabled': False,
                    'slide_enabled': False,
                    'scale_enabled': False
                }
            )
        }
    
    def _initialize_default_layouts(self) -> None:
        """Initialisiert Standard-Layouts"""
        self.default_layouts = {
            'default': LayoutConfiguration(
                name='default',
                display_name='Standard Layout',
                panels=['chat', 'thought_stream', 'system_monitor', 'settings'],
                panel_positions={
                    'chat': {'x': 0, 'y': 0, 'width': 60, 'height': 70},
                    'thought_stream': {'x': 60, 'y': 0, 'width': 40, 'height': 50},
                    'system_monitor': {'x': 60, 'y': 50, 'width': 40, 'height': 30},
                    'settings': {'x': 0, 'y': 70, 'width': 100, 'height': 30}
                },
                default_sizes={
                    'window': {'width': 1200, 'height': 800},
                    'sidebar': {'width': 300, 'height': 800},
                    'main': {'width': 900, 'height': 800}
                }
            ),
            'compact': LayoutConfiguration(
                name='compact',
                display_name='Kompakt',
                panels=['chat', 'thought_stream'],
                panel_positions={
                    'chat': {'x': 0, 'y': 0, 'width': 70, 'height': 100},
                    'thought_stream': {'x': 70, 'y': 0, 'width': 30, 'height': 100}
                },
                default_sizes={
                    'window': {'width': 800, 'height': 600},
                    'sidebar': {'width': 200, 'height': 600},
                    'main': {'width': 600, 'height': 600}
                }
            ),
            'floating': LayoutConfiguration(
                name='floating',
                display_name='Floating Windows',
                panels=['chat', 'thought_stream', 'system_monitor', 'settings'],
                panel_positions={
                    'chat': {'x': 100, 'y': 100, 'width': 400, 'height': 300},
                    'thought_stream': {'x': 520, 'y': 100, 'width': 300, 'height': 200},
                    'system_monitor': {'x': 200, 'y': 420, 'width': 350, 'height': 200},
                    'settings': {'x': 570, 'y': 320, 'width': 300, 'height': 250}
                },
                default_sizes={
                    'window': {'width': 900, 'height': 700},
                    'sidebar': {'width': 250, 'height': 700},
                    'main': {'width': 650, 'height': 700}
                }
            )
        }
    
    def _load_settings(self) -> None:
        """Lädt Einstellungen aus Dateien"""
        # Lade Haupt-Einstellungen
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                
                # Update current values
                for key, saved_value in saved_settings.items():
                    if key in self.default_settings:
                        self.default_settings[key].current_value = saved_value
                
                logger.info(f"Einstellungen geladen: {len(saved_settings)} Optionen")
            except Exception as e:
                logger.error(f"Fehler beim Laden der Einstellungen: {e}")
        
        # Lade Themes
        if self.themes_file.exists():
            try:
                with open(self.themes_file, 'r', encoding='utf-8') as f:
                    saved_themes = json.load(f)
                    # TODO: Theme-Loading implementieren
                logger.info("Themes geladen")
            except Exception as e:
                logger.error(f"Fehler beim Laden der Themes: {e}")
        
        # Lade Layouts
        if self.layouts_file.exists():
            try:
                with open(self.layouts_file, 'r', encoding='utf-8') as f:
                    saved_layouts = json.load(f)
                    # TODO: Layout-Loading implementieren
                logger.info("Layouts geladen")
            except Exception as e:
                logger.error(f"Fehler beim Laden der Layouts: {e}")
        
        # Setze aktuelle Werte
        self.settings = {key: setting.current_value for key, setting in self.default_settings.items()}
        self.themes = self.default_themes.copy()
        self.layouts = self.default_layouts.copy()
    
    def save_settings(self) -> None:
        """Speichert alle Einstellungen"""
        try:
            # Speichere Haupt-Einstellungen
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False, default=str)
            
            # Speichere Themes
            themes_data = {name: asdict(theme) for name, theme in self.themes.items()}
            with open(self.themes_file, 'w', encoding='utf-8') as f:
                json.dump(themes_data, f, indent=2, ensure_ascii=False)
            
            # Speichere Layouts
            layouts_data = {name: asdict(layout) for name, layout in self.layouts.items()}
            with open(self.layouts_file, 'w', encoding='utf-8') as f:
                json.dump(layouts_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Alle Einstellungen gespeichert")
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Einstellungen: {e}")
    
    def get_setting(self, key: str) -> Any:
        """Liefert Einstellungs-Wert"""
        return self.settings.get(key, self.default_settings.get(key, {}).get('default_value'))
    
    def set_setting(self, key: str, value: Any) -> bool:
        """Setzt Einstellungs-Wert"""
        if key not in self.default_settings:
            logger.warning(f"Unbekannte Einstellung: {key}")
            return False
        
        setting_def = self.default_settings[key]
        
        # Validiere Wert
        if not self._validate_setting_value(setting_def, value):
            logger.error(f"Ungültiger Wert für {key}: {value}")
            return False
        
        # Setze Wert
        old_value = self.settings.get(key)
        self.settings[key] = value
        setting_def.current_value = value
        
        # Triggere Callbacks
        self._notify_setting_changed(key, old_value, value)
        
        # Auto-Save
        self.save_settings()
        
        logger.info(f"Einstellung geändert: {key} = {value}")
        return True
    
    def _validate_setting_value(self, setting_def: SettingOption, value: Any) -> bool:
        """Validiert Einstellungs-Wert"""
        try:
            # Typ-Validierung
            if setting_def.value_type == 'bool':
                return isinstance(value, bool)
            elif setting_def.value_type == 'int':
                if not isinstance(value, int):
                    return False
                if setting_def.min_value is not None and value < setting_def.min_value:
                    return False
                if setting_def.max_value is not None and value > setting_def.max_value:
                    return False
            elif setting_def.value_type == 'float':
                if not isinstance(value, (int, float)):
                    return False
                if setting_def.min_value is not None and value < setting_def.min_value:
                    return False
                if setting_def.max_value is not None and value > setting_def.max_value:
                    return False
            elif setting_def.value_type == 'string':
                if not isinstance(value, str):
                    return False
                if setting_def.options and value not in setting_def.options:
                    return False
            
            return True
            
        except Exception:
            return False
    
    def _notify_setting_changed(self, key: str, old_value: Any, new_value: Any) -> None:
        """Benachrichtigt über Einstellungs-Änderungen"""
        for callback in self.change_callbacks:
            try:
                callback(key, old_value, new_value)
            except Exception as e:
                logger.error(f"Settings Callback Fehler: {e}")
    
    def register_change_callback(self, callback: Callable[[str, Any, Any], None]) -> None:
        """Registriert Callback für Einstellungs-Änderungen"""
        self.change_callbacks.append(callback)
    
    def get_settings_by_category(self, category: str) -> Dict[str, SettingOption]:
        """Liefert Einstellungen nach Kategorie"""
        return {
            key: setting for key, setting in self.default_settings.items()
            if setting.category == category
        }
    
    def get_all_categories(self) -> List[str]:
        """Liefert alle Einstellungs-Kategorien"""
        categories = set()
        for setting in self.default_settings.values():
            categories.add(setting.category)
        return sorted(list(categories))
    
    def reset_setting(self, key: str) -> bool:
        """Setzt Einstellung auf Standard zurück"""
        if key not in self.default_settings:
            return False
        
        default_value = self.default_settings[key].default_value
        return self.set_setting(key, default_value)
    
    def reset_category(self, category: str) -> None:
        """Setzt alle Einstellungen einer Kategorie zurück"""
        for key, setting in self.default_settings.items():
            if setting.category == category:
                self.reset_setting(key)
    
    def reset_all_settings(self) -> None:
        """Setzt alle Einstellungen zurück"""
        for key in self.default_settings.keys():
            self.reset_setting(key)
    
    def export_settings(self, file_path: str) -> bool:
        """Exportiert Einstellungen in Datei"""
        try:
            export_data = {
                'settings': self.settings,
                'current_theme': self.current_theme,
                'current_layout': self.current_layout,
                'export_timestamp': datetime.now().isoformat()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Einstellungen exportiert nach: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Export-Fehler: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Importiert Einstellungen aus Datei"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'settings' in import_data:
                for key, value in import_data['settings'].items():
                    self.set_setting(key, value)
            
            if 'current_theme' in import_data:
                self.current_theme = import_data['current_theme']
            
            if 'current_layout' in import_data:
                self.current_layout = import_data['current_layout']
            
            logger.info(f"Einstellungen importiert von: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Import-Fehler: {e}")
            return False
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """Liefert Zusammenfassung der aktuellen Einstellungen"""
        return {
            'total_settings': len(self.settings),
            'categories': len(self.get_all_categories()),
            'current_theme': self.current_theme,
            'current_layout': self.current_layout,
            'advanced_settings_count': sum(1 for s in self.default_settings.values() if s.advanced),
            'settings_requiring_restart': [
                key for key, setting in self.default_settings.items() 
                if setting.requires_restart and self.settings.get(key) != setting.default_value
            ]
        }

if __name__ == "__main__":
    # Test der Extended Settings Engine
    settings_engine = ExtendedSettingsEngine()
    
    # Test Einstellung setzen
    settings_engine.set_setting('ai_response_temperature', 0.8)
    
    # Test Kategorien abrufen
    categories = settings_engine.get_all_categories()
    print("Verfügbare Kategorien:", categories)
    
    # Test Einstellungen nach Kategorie
    ai_settings = settings_engine.get_settings_by_category('AI & Intelligenz')
    print(f"AI Einstellungen: {len(ai_settings)}")
    
    # Test Summary
    summary = settings_engine.get_settings_summary()
    print("Settings Summary:", json.dumps(summary, indent=2))
