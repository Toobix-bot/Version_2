"""
Toobix System Organizer - Erweiterte Organisations-Engine
Komplette System-Reorganisation mit KI-gestützter Analyse
"""
import os
import shutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import psutil

class AdvancedSystemOrganizer:
    """Erweiterte System-Organisations-Engine für Toobix"""
    
    def __init__(self):
        self.user_home = Path.home()
        self.organization_config = {
            'structure': self._get_default_structure(),
            'rules': self._get_organization_rules(),
            'priorities': self._get_cleanup_priorities()
        }
        self.scan_results = {}
        print("🏗️ Advanced System Organizer initialisiert")
    
    def _get_default_structure(self) -> Dict:
        """Definiert die Master-Ordnerstruktur"""
        return {
            '_ORGANISATION': {
                '_DAILY_WORK': ['Heute', 'Diese_Woche', 'Wichtig', 'Review'],
                '_PROJEKTE': ['Aktiv', 'Wartend', 'Abgeschlossen', 'Ideen'],
                '_ARCHIV': ['2024', '2025', 'Alt_Wichtig', 'Referenz'],
                '_TEMP_SORTING': ['Unsortiert', 'Zu_Pruefen', 'Backup_Alt']
            },
            'ENTWICKLUNG': {
                'Python': ['Scripts', 'Projekte', 'Libraries', 'Learning'],
                'WebDev': ['Frontend', 'Backend', 'APIs', 'Databases'],
                'Tools': ['IDEs', 'Utilities', 'Configs', 'Extensions'],
                'Archives': ['Old_Projects', 'Deprecated', 'Learning']
            },
            'DOKUMENTE': {
                'Geschaeftlich': ['Rechnungen', 'Vertraege', 'Korrespondenz'],
                'Persoenlich': ['Zertifikate', 'Gesundheit', 'Hobbys'],
                'Finanzen': ['Steuern', 'Bankdaten', 'Investments'],
                'Vorlagen': ['Briefe', 'Praesentationen', 'Formulare']
            },
            'MEDIEN': {
                'Fotos': ['2024', '2025', 'Familie', 'Reisen', 'Screenshots'],
                'Videos': ['Projekte', 'Tutorials', 'Persoenlich'],
                'Musik': ['Playlists', 'Projekte', 'Samples'],
                'Design': ['Logos', 'Templates', 'Resources']
            },
            'SYSTEM': {
                'Backups': ['System', 'Dokumente', 'Projekte', 'Configs'],
                'Configs': ['Apps', 'System', 'Development', 'Backup'],
                'Software': ['Portable', 'Installers', 'Updates'],
                'Drivers': ['Hardware', 'Backup', 'Updates']
            }
        }
    
    def _get_organization_rules(self) -> Dict:
        """Definiert Organisations-Regeln"""
        return {
            'file_extensions': {
                'code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.php'],
                'documents': ['.pdf', '.doc', '.docx', '.txt', '.md', '.rtf'],
                'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
                'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
                'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
                'archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
                'executables': ['.exe', '.msi', '.dmg', '.deb', '.rpm']
            },
            'folder_patterns': {
                'projects': ['node_modules', '.git', '.venv', '__pycache__'],
                'temp': ['temp', 'tmp', 'cache', 'log'],
                'backup': ['backup', 'bak', 'old', 'archive']
            },
            'size_thresholds': {
                'large_file': 100 * 1024 * 1024,  # 100MB
                'huge_file': 1024 * 1024 * 1024,  # 1GB
                'folder_warning': 10 * 1024 * 1024 * 1024  # 10GB
            }
        }
    
    def _get_cleanup_priorities(self) -> List:
        """Definiert Aufräum-Prioritäten"""
        return [
            {'name': 'temp_files', 'priority': 1, 'safe': True},
            {'name': 'browser_cache', 'priority': 2, 'safe': True},
            {'name': 'recycle_bin', 'priority': 3, 'safe': True},
            {'name': 'old_downloads', 'priority': 4, 'safe': False},
            {'name': 'duplicate_files', 'priority': 5, 'safe': False},
            {'name': 'large_logs', 'priority': 6, 'safe': False}
        ]
    
    def analyze_system_comprehensive(self) -> Dict:
        """Umfassende System-Analyse"""
        print("🔍 Starte umfassende System-Analyse...")
        
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'system_health': self._analyze_system_health(),
            'storage_analysis': self._analyze_storage(),
            'folder_structure': self._analyze_folder_structure(),
            'file_distribution': self._analyze_file_distribution(),
            'cleanup_opportunities': self._find_cleanup_opportunities(),
            'organization_suggestions': self._generate_organization_suggestions()
        }
        
        self.scan_results = analysis
        print("✅ System-Analyse abgeschlossen")
        return analysis
    
    def _analyze_system_health(self) -> Dict:
        """Analysiert System-Gesundheit"""
        try:
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            cpu_percent = psutil.cpu_percent(interval=1)
            
            health_score = 100
            warnings = []
            
            # RAM-Check
            if memory.percent > 85:
                health_score -= 30
                warnings.append(f"Kritischer RAM-Verbrauch: {memory.percent:.1f}%")
            elif memory.percent > 70:
                health_score -= 15
                warnings.append(f"Hoher RAM-Verbrauch: {memory.percent:.1f}%")
            
            # Disk-Check
            if disk.percent > 90:
                health_score -= 25
                warnings.append(f"Kritischer Speicherplatz: {disk.percent:.1f}%")
            elif disk.percent > 80:
                health_score -= 10
                warnings.append(f"Wenig Speicherplatz: {disk.percent:.1f}%")
            
            # CPU-Check
            if cpu_percent > 80:
                health_score -= 20
                warnings.append(f"Hohe CPU-Auslastung: {cpu_percent:.1f}%")
            
            status = "excellent" if health_score >= 90 else \
                    "good" if health_score >= 70 else \
                    "warning" if health_score >= 50 else "critical"
            
            return {
                'score': health_score,
                'status': status,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
                'cpu_percent': cpu_percent,
                'warnings': warnings,
                'free_space_gb': disk.free / (1024**3)
            }
            
        except Exception as e:
            return {'error': f"System-Health-Analyse fehlgeschlagen: {e}"}
    
    def _analyze_storage(self) -> Dict:
        """Analysiert Speicher-Verteilung"""
        try:
            storage_info = {}
            main_folders = ['Desktop', 'Documents', 'Downloads', 'Pictures', 'Videos', 'Music']
            
            for folder in main_folders:
                folder_path = self.user_home / folder
                if folder_path.exists():
                    size = self._get_folder_size(folder_path)
                    file_count = self._count_files(folder_path)
                    storage_info[folder] = {
                        'size_mb': size / (1024 * 1024),
                        'size_gb': size / (1024 * 1024 * 1024),
                        'file_count': file_count,
                        'avg_file_size': size / file_count if file_count > 0 else 0
                    }
            
            return storage_info
            
        except Exception as e:
            return {'error': f"Storage-Analyse fehlgeschlagen: {e}"}
    
    def _analyze_folder_structure(self) -> Dict:
        """Analysiert Ordnerstruktur"""
        try:
            structure_analysis = {
                'depth_analysis': {},
                'naming_patterns': {},
                'organization_score': 0,
                'suggestions': []
            }
            
            # Analysiere Haupt-Ordner
            for folder_name in ['Desktop', 'Documents', 'Downloads']:
                folder_path = self.user_home / folder_name
                if folder_path.exists():
                    depth_map = self._analyze_folder_depth(folder_path)
                    structure_analysis['depth_analysis'][folder_name] = depth_map
                    
                    # Bewerte Organisation
                    org_score = self._score_folder_organization(folder_path)
                    structure_analysis[f'{folder_name}_score'] = org_score
            
            # Generiere Verbesserungsvorschläge
            suggestions = self._generate_structure_suggestions(structure_analysis)
            structure_analysis['suggestions'] = suggestions
            
            return structure_analysis
            
        except Exception as e:
            return {'error': f"Struktur-Analyse fehlgeschlagen: {e}"}
    
    def _analyze_file_distribution(self) -> Dict:
        """Analysiert Datei-Verteilung nach Typen"""
        try:
            file_types = {}
            rules = self.organization_config['rules']['file_extensions']
            
            for category, extensions in rules.items():
                file_types[category] = {
                    'count': 0,
                    'total_size': 0,
                    'locations': set()
                }
            
            file_types['other'] = {'count': 0, 'total_size': 0, 'locations': set()}
            
            # Scanne wichtige Ordner
            scan_folders = [
                self.user_home / 'Desktop',
                self.user_home / 'Documents', 
                self.user_home / 'Downloads'
            ]
            
            for folder in scan_folders:
                if folder.exists():
                    self._scan_folder_for_types(folder, file_types, rules)
            
            # Konvertiere sets zu lists für JSON-Serialisierung
            for category in file_types:
                file_types[category]['locations'] = list(file_types[category]['locations'])
                file_types[category]['avg_size'] = (
                    file_types[category]['total_size'] / file_types[category]['count']
                    if file_types[category]['count'] > 0 else 0
                )
            
            return file_types
            
        except Exception as e:
            return {'error': f"Datei-Verteilungs-Analyse fehlgeschlagen: {e}"}
    
    def _find_cleanup_opportunities(self) -> List[Dict]:
        """Findet Aufräum-Möglichkeiten"""
        opportunities = []
        
        try:
            # Temp-Dateien
            temp_size = self._estimate_temp_files()
            if temp_size > 50 * 1024 * 1024:  # > 50MB
                opportunities.append({
                    'type': 'temp_files',
                    'description': 'Temporäre Dateien löschen',
                    'estimated_savings_mb': temp_size / (1024 * 1024),
                    'safety': 'safe',
                    'priority': 1
                })
            
            # Downloads-Ordner
            downloads_path = self.user_home / 'Downloads'
            if downloads_path.exists():
                old_downloads = self._find_old_downloads(downloads_path)
                if old_downloads['size'] > 100 * 1024 * 1024:  # > 100MB
                    opportunities.append({
                        'type': 'old_downloads',
                        'description': f'{old_downloads["count"]} alte Downloads',
                        'estimated_savings_mb': old_downloads['size'] / (1024 * 1024),
                        'safety': 'review_needed',
                        'priority': 3
                    })
            
            # Desktop-Chaos
            desktop_path = self.user_home / 'Desktop'
            if desktop_path.exists():
                desktop_files = list(desktop_path.iterdir())
                if len(desktop_files) > 20:
                    opportunities.append({
                        'type': 'desktop_cleanup',
                        'description': f'{len(desktop_files)} Dateien auf Desktop organisieren',
                        'estimated_savings_mb': 0,  # Organisation, kein Speicher
                        'safety': 'safe',
                        'priority': 2
                    })
            
            return sorted(opportunities, key=lambda x: x['priority'])
            
        except Exception as e:
            return [{'error': f"Cleanup-Analyse fehlgeschlagen: {e}"}]
    
    def _generate_organization_suggestions(self) -> List[Dict]:
        """Generiert Organisations-Vorschläge"""
        suggestions = []
        
        try:
            # Vorschlag 1: Master-Struktur erstellen
            suggestions.append({
                'type': 'create_master_structure',
                'title': 'Master-Ordnerstruktur erstellen',
                'description': 'Professionelle Ordnerstruktur für maximale Organisation',
                'impact': 'high',
                'effort': 'medium',
                'priority': 1
            })
            
            # Vorschlag 2: Desktop aufräumen
            desktop_path = self.user_home / 'Desktop'
            if desktop_path.exists():
                desktop_files = list(desktop_path.iterdir())
                if len(desktop_files) > 10:
                    suggestions.append({
                        'type': 'organize_desktop',
                        'title': 'Desktop organisieren',
                        'description': f'{len(desktop_files)} Dateien strukturiert ablegen',
                        'impact': 'medium',
                        'effort': 'low',
                        'priority': 2
                    })
            
            # Vorschlag 3: Downloads strukturieren
            downloads_path = self.user_home / 'Downloads'
            if downloads_path.exists():
                download_files = list(downloads_path.iterdir())
                if len(download_files) > 20:
                    suggestions.append({
                        'type': 'organize_downloads',
                        'title': 'Downloads strukturieren',
                        'description': f'{len(download_files)} Downloads kategorisieren',
                        'impact': 'medium',
                        'effort': 'medium',
                        'priority': 3
                    })
            
            return suggestions
            
        except Exception as e:
            return [{'error': f"Suggestions-Generierung fehlgeschlagen: {e}"}]
    
    def create_master_structure(self, base_path: Optional[Path] = None) -> Dict:
        """Erstellt die Master-Ordnerstruktur"""
        if base_path is None:
            base_path = self.user_home / "TOOBIX_ORGANISATION"
        
        created_folders = []
        errors = []
        
        try:
            print(f"🏗️ Erstelle Master-Struktur in: {base_path}")
            
            structure = self.organization_config['structure']
            
            for main_folder, sub_structure in structure.items():
                main_path = base_path / main_folder
                
                try:
                    main_path.mkdir(parents=True, exist_ok=True)
                    created_folders.append(str(main_path))
                    
                    if isinstance(sub_structure, dict):
                        for sub_folder, sub_sub_folders in sub_structure.items():
                            sub_path = main_path / sub_folder
                            sub_path.mkdir(exist_ok=True)
                            created_folders.append(str(sub_path))
                            
                            if isinstance(sub_sub_folders, list):
                                for sub_sub_folder in sub_sub_folders:
                                    sub_sub_path = sub_path / sub_sub_folder
                                    sub_sub_path.mkdir(exist_ok=True)
                                    created_folders.append(str(sub_sub_path))
                    
                except Exception as e:
                    errors.append(f"Fehler bei {main_folder}: {e}")
            
            # Erstelle README-Datei
            readme_content = self._generate_structure_readme()
            readme_path = base_path / "README_ORGANISATION.md"
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            result = {
                'success': True,
                'base_path': str(base_path),
                'created_folders': created_folders,
                'folder_count': len(created_folders),
                'errors': errors
            }
            
            print(f"✅ Master-Struktur erstellt: {len(created_folders)} Ordner")
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Master-Struktur-Erstellung fehlgeschlagen: {e}",
                'created_folders': created_folders,
                'errors': errors
            }
    
    def execute_comprehensive_organization(self) -> Dict:
        """Führt komplette System-Organisation durch"""
        print("🚀 Starte komplette System-Organisation...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'phases': {},
            'overall_success': True,
            'total_time': 0
        }
        
        start_time = datetime.now()
        
        try:
            # Phase 1: System-Analyse
            print("📊 Phase 1: System-Analyse...")
            analysis = self.analyze_system_comprehensive()
            results['phases']['analysis'] = {
                'success': 'error' not in analysis,
                'data': analysis
            }
            
            # Phase 2: Master-Struktur erstellen
            print("🏗️ Phase 2: Master-Struktur erstellen...")
            structure_result = self.create_master_structure()
            results['phases']['structure'] = structure_result
            
            # Phase 3: Aufräum-Opportunitäten umsetzen
            print("🧹 Phase 3: Aufräumung durchführen...")
            cleanup_result = self._execute_safe_cleanup()
            results['phases']['cleanup'] = cleanup_result
            
            # Phase 4: Automation einrichten
            print("⚙️ Phase 4: Automation konfigurieren...")
            automation_result = self._setup_organization_automation()
            results['phases']['automation'] = automation_result
            
            end_time = datetime.now()
            results['total_time'] = (end_time - start_time).total_seconds()
            
            print("✅ Komplette System-Organisation abgeschlossen!")
            return results
            
        except Exception as e:
            results['overall_success'] = False
            results['error'] = f"Organisation fehlgeschlagen: {e}"
            return results
    
    # Helper-Methoden
    def _get_folder_size(self, folder_path: Path) -> int:
        """Berechnet Ordnergröße"""
        total_size = 0
        try:
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except:
            pass
        return total_size
    
    def _count_files(self, folder_path: Path) -> int:
        """Zählt Dateien in Ordner"""
        try:
            return len([f for f in folder_path.rglob('*') if f.is_file()])
        except:
            return 0
    
    def _estimate_temp_files(self) -> int:
        """Schätzt Größe temporärer Dateien"""
        try:
            temp_paths = [
                Path.home() / "AppData" / "Local" / "Temp",
                Path("C:/Windows/Temp"),
                Path("C:/Temp")
            ]
            
            total_size = 0
            for path in temp_paths:
                if path.exists():
                    total_size += self._get_folder_size(path)
            
            return total_size
        except:
            return 0
    
    def _generate_structure_readme(self) -> str:
        """Generiert README für Ordnerstruktur"""
        return f"""# TOOBIX MASTER-ORGANISATIONS-STRUKTUR

Erstellt am: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

## 📋 ÜBERSICHT
Diese Struktur wurde von Toobix AI Assistant erstellt für maximale Produktivität und Organisation.

## 🏗️ STRUKTUR-BESCHREIBUNG

### 🏠 _ORGANISATION/
Zentrale Arbeitsorganisation
- **_DAILY_WORK/**: Tägliche Arbeitsdateien
- **_PROJEKTE/**: Aktive Projekte nach Status
- **_ARCHIV/**: Wichtige alte Dateien
- **_TEMP_SORTING/**: Temporäre Sortierungshilfe

### 💻 ENTWICKLUNG/
Alle development-bezogenen Inhalte
- **Python/**: Python-Projekte und Scripts
- **WebDev/**: Web-Development-Projekte
- **Tools/**: Entwicklungstools und Configs

### 📄 DOKUMENTE/
Dokumenten-Management
- **Geschaeftlich/**: Business-Dokumente
- **Persoenlich/**: Private Dokumente
- **Finanzen/**: Finanz-Dokumente

### 🎨 MEDIEN/
Multimedia-Inhalte organisiert

### 💾 SYSTEM/
System-relevante Dateien und Backups

## 🎯 VERWENDUNG
1. Neue Dateien sofort in passende Kategorie einordnen
2. _TEMP_SORTING für unklare Zuordnung nutzen
3. Regelmäßig Archive aktualisieren
4. Backup-Routinen befolgen

## 🤖 TOOBIX AUTOMATION
Diese Struktur unterstützt Toobix Automation für:
- Automatische Dateisortierung
- Backup-Routinen
- Cleanup-Prozesse
- Monitoring

Erstellt von: Toobix AI Assistant
"""
    
    def _execute_safe_cleanup(self) -> Dict:
        """Führt sichere Aufräumung durch"""
        # Placeholder für sichere Cleanup-Operationen
        return {
            'success': True,
            'actions_performed': [],
            'space_freed_mb': 0,
            'message': 'Sichere Aufräumung bereit für Implementierung'
        }
    
    def _setup_organization_automation(self) -> Dict:
        """Richtet Organisations-Automation ein"""
        # Placeholder für Automation-Setup
        return {
            'success': True,
            'automations_created': [],
            'message': 'Automation-Setup bereit für Implementierung'
        }
    
    def _analyze_folder_depth(self, folder_path: Path) -> Dict:
        """Analysiert Ordner-Tiefe"""
        depth_map = {}
        try:
            for item in folder_path.rglob('*'):
                if item.is_dir():
                    depth = len(item.relative_to(folder_path).parts)
                    depth_map[depth] = depth_map.get(depth, 0) + 1
        except:
            pass
        return depth_map
    
    def _score_folder_organization(self, folder_path: Path) -> int:
        """Bewertet Ordner-Organisation (0-100)"""
        score = 50  # Basis-Score
        
        try:
            items = list(folder_path.iterdir())
            files = [item for item in items if item.is_file()]
            folders = [item for item in items if item.is_dir()]
            
            # Bewertungskriterien
            if len(files) < 10:  # Wenige lose Dateien = gut
                score += 20
            elif len(files) > 50:  # Viele lose Dateien = schlecht
                score -= 30
            
            if len(folders) > 0:  # Ordner vorhanden = gut
                score += 10
            
            # Naming-Konventionen prüfen
            good_names = sum(1 for item in items if '_' in item.name or '-' in item.name)
            if good_names > len(items) * 0.5:
                score += 10
            
        except:
            pass
        
        return max(0, min(100, score))
    
    def _scan_folder_for_types(self, folder: Path, file_types: Dict, rules: Dict):
        """Scannt Ordner nach Dateitypen"""
        try:
            for file_path in folder.rglob('*'):
                if file_path.is_file():
                    extension = file_path.suffix.lower()
                    file_size = file_path.stat().st_size
                    
                    categorized = False
                    for category, extensions in rules.items():
                        if extension in extensions:
                            file_types[category]['count'] += 1
                            file_types[category]['total_size'] += file_size
                            file_types[category]['locations'].add(str(file_path.parent))
                            categorized = True
                            break
                    
                    if not categorized:
                        file_types['other']['count'] += 1
                        file_types['other']['total_size'] += file_size
                        file_types['other']['locations'].add(str(file_path.parent))
        except:
            pass
    
    def _find_old_downloads(self, downloads_path: Path) -> Dict:
        """Findet alte Downloads"""
        old_downloads = {'count': 0, 'size': 0, 'files': []}
        
        try:
            cutoff_days = 30
            cutoff_timestamp = datetime.now().timestamp() - (cutoff_days * 24 * 60 * 60)
            
            for item in downloads_path.iterdir():
                if item.is_file():
                    if item.stat().st_mtime < cutoff_timestamp:
                        old_downloads['count'] += 1
                        old_downloads['size'] += item.stat().st_size
                        old_downloads['files'].append(str(item))
        except:
            pass
        
        return old_downloads
    
    def _generate_structure_suggestions(self, structure_analysis: Dict) -> List[str]:
        """Generiert Struktur-Verbesserungsvorschläge"""
        suggestions = []
        
        try:
            for folder_name, depth_map in structure_analysis.get('depth_analysis', {}).items():
                if not depth_map:  # Leerer Ordner
                    suggestions.append(f"{folder_name}: Ordner ist leer - Organisation empfohlen")
                elif max(depth_map.keys()) > 5:  # Zu tiefe Verschachtelung
                    suggestions.append(f"{folder_name}: Zu tiefe Ordnerstruktur - Vereinfachung empfohlen")
                elif 1 not in depth_map:  # Keine Unterordner
                    suggestions.append(f"{folder_name}: Keine Unterordner - Strukturierung empfohlen")
        except:
            pass
        
        return suggestions

# Globale Instanz für Toobix
system_organizer = AdvancedSystemOrganizer()
