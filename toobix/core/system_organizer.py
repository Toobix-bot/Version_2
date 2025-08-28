"""
Toobix System Organizer
Sichere System-Aufräum- und Organisationsfunktionen
"""
import os
import shutil
import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json

class SystemOrganizer:
    """Sichere System-Organisation und Aufräumung"""
    
    def __init__(self, settings):
        self.settings = settings
        
        # Sichere Standardverzeichnisse für Aufräumung
        self.safe_cleanup_dirs = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            "C:/Users/Public/Desktop",
            "C:/Temp",
            "C:/Windows/Temp",
            os.path.expanduser("~/AppData/Local/Temp")
        ]
        
        # Wichtige Verzeichnisse die NIEMALS gelöscht werden
        self.protected_dirs = [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Videos"),
            os.path.expanduser("~/Music"),
            "C:/Program Files",
            "C:/Program Files (x86)",
            "C:/Windows",
            "C:/Users",
            os.path.expanduser("~/.ssh"),
            os.path.expanduser("~/OneDrive")
        ]
        
        # Sichere Dateierweiterungen für automatische Sortierung
        self.file_categories = {
            'Dokumente': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'Bilder': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
            'Archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Programme': ['.exe', '.msi', '.deb', '.dmg'],
            'Tabellen': ['.xlsx', '.xls', '.csv', '.ods']
        }
        
        print("🧹 System Organizer initialisiert")
    
    def analyze_system_mess(self) -> Dict[str, any]:
        """Analysiert das System und findet Aufräum-Möglichkeiten"""
        analysis = {
            'messy_directories': [],
            'large_files': [],
            'duplicate_candidates': [],
            'temp_files': [],
            'old_downloads': [],
            'disk_usage': {},
            'recommendations': []
        }
        
        print("🔍 Analysiere System...")
        
        # Downloads-Ordner analysieren
        downloads_dir = os.path.expanduser("~/Downloads")
        if os.path.exists(downloads_dir):
            analysis['old_downloads'] = self._find_old_downloads(downloads_dir)
        
        # Desktop analysieren
        desktop_dir = os.path.expanduser("~/Desktop")
        if os.path.exists(desktop_dir):
            desktop_files = self._count_files_in_directory(desktop_dir)
            if desktop_files > 20:
                analysis['messy_directories'].append({
                    'path': desktop_dir,
                    'file_count': desktop_files,
                    'reason': 'Viele Dateien auf Desktop'
                })
        
        # Temp-Dateien finden
        analysis['temp_files'] = self._find_temp_files()
        
        # Große Dateien finden
        analysis['large_files'] = self._find_large_files()
        
        # Festplatten-Nutzung
        analysis['disk_usage'] = self._get_disk_usage()
        
        # Empfehlungen generieren
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _find_old_downloads(self, downloads_dir: str) -> List[Dict]:
        """Findet alte Downloads die aufgeräumt werden können"""
        old_files = []
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=30)
        
        try:
            for file_path in Path(downloads_dir).rglob('*'):
                if file_path.is_file():
                    stat = file_path.stat()
                    modified_time = datetime.datetime.fromtimestamp(stat.st_mtime)
                    
                    if modified_time < cutoff_date:
                        old_files.append({
                            'path': str(file_path),
                            'size_mb': round(stat.st_size / (1024*1024), 2),
                            'modified': modified_time.strftime('%d.%m.%Y'),
                            'safe_to_move': self._is_safe_to_move(file_path)
                        })
        except Exception as e:
            print(f"⚠️ Fehler beim Analysieren von Downloads: {e}")
        
        return sorted(old_files, key=lambda x: x['size_mb'], reverse=True)[:50]
    
    def _find_temp_files(self) -> List[Dict]:
        """Findet temporäre Dateien die gelöscht werden können"""
        temp_files = []
        temp_dirs = [
            "C:/Windows/Temp",
            os.path.expanduser("~/AppData/Local/Temp"),
            "C:/Temp"
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for file_path in Path(temp_dir).rglob('*'):
                        if file_path.is_file():
                            stat = file_path.stat()
                            temp_files.append({
                                'path': str(file_path),
                                'size_mb': round(stat.st_size / (1024*1024), 2),
                                'directory': temp_dir
                            })
                except Exception as e:
                    print(f"⚠️ Fehler beim Scannen von {temp_dir}: {e}")
        
        return sorted(temp_files, key=lambda x: x['size_mb'], reverse=True)[:100]
    
    def _find_large_files(self) -> List[Dict]:
        """Findet große Dateien die überprüft werden sollten"""
        large_files = []
        search_dirs = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents")
        ]
        
        for search_dir in search_dirs:
            if os.path.exists(search_dir):
                try:
                    for file_path in Path(search_dir).rglob('*'):
                        if file_path.is_file():
                            stat = file_path.stat()
                            size_mb = stat.st_size / (1024*1024)
                            
                            if size_mb > 100:  # Größer als 100MB
                                large_files.append({
                                    'path': str(file_path),
                                    'size_mb': round(size_mb, 2),
                                    'size_gb': round(size_mb / 1024, 2),
                                    'extension': file_path.suffix.lower()
                                })
                except Exception as e:
                    print(f"⚠️ Fehler beim Suchen großer Dateien in {search_dir}: {e}")
        
        return sorted(large_files, key=lambda x: x['size_mb'], reverse=True)[:20]
    
    def _get_disk_usage(self) -> Dict:
        """Ermittelt Festplatten-Nutzung"""
        import psutil
        
        usage = {}
        try:
            for partition in psutil.disk_partitions():
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    usage[partition.device] = {
                        'total_gb': round(partition_usage.total / (1024**3), 2),
                        'used_gb': round(partition_usage.used / (1024**3), 2),
                        'free_gb': round(partition_usage.free / (1024**3), 2),
                        'percent_used': round((partition_usage.used / partition_usage.total) * 100, 1)
                    }
                except PermissionError:
                    continue
        except Exception as e:
            print(f"⚠️ Fehler beim Ermitteln der Festplatten-Nutzung: {e}")
        
        return usage
    
    def _count_files_in_directory(self, directory: str) -> int:
        """Zählt Dateien in einem Verzeichnis"""
        try:
            return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        except:
            return 0
    
    def _is_safe_to_move(self, file_path: Path) -> bool:
        """Prüft ob eine Datei sicher verschoben werden kann"""
        # Prüfe auf wichtige Dateierweiterungen
        dangerous_extensions = ['.exe', '.msi', '.bat', '.cmd', '.ps1', '.reg']
        if file_path.suffix.lower() in dangerous_extensions:
            return False
        
        # Prüfe auf System-/Programmdateien
        path_str = str(file_path).lower()
        if any(word in path_str for word in ['system', 'program', 'windows', 'driver']):
            return False
        
        return True
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generiert Aufräum-Empfehlungen"""
        recommendations = []
        
        if analysis['old_downloads']:
            old_count = len(analysis['old_downloads'])
            recommendations.append(f"📁 {old_count} alte Downloads gefunden - können in Archiv-Ordner verschoben werden")
        
        if analysis['temp_files']:
            temp_size = sum(f['size_mb'] for f in analysis['temp_files'])
            recommendations.append(f"🗑️ {temp_size:.1f} MB temporäre Dateien können gelöscht werden")
        
        if analysis['messy_directories']:
            recommendations.append("🖥️ Desktop aufräumen - viele Dateien gefunden")
        
        if analysis['large_files']:
            large_size = sum(f['size_gb'] for f in analysis['large_files'])
            recommendations.append(f"📊 {large_size:.1f} GB in großen Dateien - überprüfen empfohlen")
        
        # Festplatten-Warnung
        for device, usage in analysis['disk_usage'].items():
            if usage['percent_used'] > 85:
                recommendations.append(f"⚠️ Festplatte {device} zu {usage['percent_used']}% voll")
        
        return recommendations
    
    def create_safe_cleanup_plan(self, analysis: Dict) -> Dict:
        """Erstellt einen sicheren Aufräumplan"""
        plan = {
            'actions': [],
            'estimated_space_gb': 0,
            'safety_level': 'high',
            'backup_recommended': True
        }
        
        # Temp-Dateien löschen (sehr sicher)
        if analysis['temp_files']:
            temp_size_gb = sum(f['size_mb'] for f in analysis['temp_files']) / 1024
            plan['actions'].append({
                'type': 'delete_temp_files',
                'description': 'Temporäre Dateien löschen',
                'files': analysis['temp_files'],
                'space_saved_gb': round(temp_size_gb, 2),
                'safety': 'sehr sicher',
                'reversible': False
            })
            plan['estimated_space_gb'] += temp_size_gb
        
        # Alte Downloads organisieren (sicher)
        if analysis['old_downloads']:
            safe_downloads = [f for f in analysis['old_downloads'] if f['safe_to_move']]
            if safe_downloads:
                plan['actions'].append({
                    'type': 'organize_downloads',
                    'description': 'Alte Downloads in Archiv-Ordner verschieben',
                    'files': safe_downloads,
                    'safety': 'sicher',
                    'reversible': True
                })
        
        # Desktop organisieren
        if analysis['messy_directories']:
            plan['actions'].append({
                'type': 'organize_desktop',
                'description': 'Desktop-Dateien nach Typ sortieren',
                'safety': 'sicher',
                'reversible': True
            })
        
        return plan
    
    def execute_safe_cleanup(self, plan: Dict, dry_run: bool = True) -> Dict:
        """Führt sicheren Aufräumplan aus"""
        results = {
            'completed_actions': [],
            'failed_actions': [],
            'space_freed_gb': 0,
            'dry_run': dry_run
        }
        
        if dry_run:
            print("🧪 Trockenlauf - keine Dateien werden tatsächlich verändert")
        
        for action in plan['actions']:
            try:
                if action['type'] == 'delete_temp_files':
                    result = self._execute_temp_cleanup(action, dry_run)
                elif action['type'] == 'organize_downloads':
                    result = self._execute_downloads_organization(action, dry_run)
                elif action['type'] == 'organize_desktop':
                    result = self._execute_desktop_organization(action, dry_run)
                else:
                    continue
                
                if result['success']:
                    results['completed_actions'].append(result)
                    if 'space_freed' in result:
                        results['space_freed_gb'] += result['space_freed']
                else:
                    results['failed_actions'].append(result)
                    
            except Exception as e:
                results['failed_actions'].append({
                    'action': action['type'],
                    'error': str(e)
                })
        
        return results
    
    def _execute_temp_cleanup(self, action: Dict, dry_run: bool) -> Dict:
        """Führt Temp-Dateien Aufräumung aus"""
        deleted_count = 0
        space_freed = 0
        
        for temp_file in action['files']:
            try:
                if not dry_run:
                    file_path = Path(temp_file['path'])
                    if file_path.exists():
                        file_path.unlink()
                
                deleted_count += 1
                space_freed += temp_file['size_mb']
                
            except Exception as e:
                print(f"⚠️ Fehler beim Löschen {temp_file['path']}: {e}")
        
        return {
            'success': True,
            'action': 'delete_temp_files',
            'deleted_files': deleted_count,
            'space_freed': space_freed / 1024  # GB
        }
    
    def _execute_downloads_organization(self, action: Dict, dry_run: bool) -> Dict:
        """Organisiert Downloads-Ordner"""
        archive_dir = os.path.expanduser("~/Downloads/Archiv")
        moved_count = 0
        
        if not dry_run:
            os.makedirs(archive_dir, exist_ok=True)
        
        for download_file in action['files']:
            try:
                if not dry_run:
                    source = Path(download_file['path'])
                    if source.exists():
                        destination = Path(archive_dir) / source.name
                        shutil.move(str(source), str(destination))
                
                moved_count += 1
                
            except Exception as e:
                print(f"⚠️ Fehler beim Verschieben {download_file['path']}: {e}")
        
        return {
            'success': True,
            'action': 'organize_downloads',
            'moved_files': moved_count,
            'archive_location': archive_dir
        }
    
    def _execute_desktop_organization(self, action: Dict, dry_run: bool) -> Dict:
        """Organisiert Desktop nach Dateitypen"""
        desktop_dir = Path(os.path.expanduser("~/Desktop"))
        organized_count = 0
        
        if not desktop_dir.exists():
            return {'success': False, 'error': 'Desktop-Ordner nicht gefunden'}
        
        # Erstelle Kategorie-Ordner
        for category in self.file_categories.keys():
            category_dir = desktop_dir / category
            if not dry_run:
                category_dir.mkdir(exist_ok=True)
        
        # Sortiere Dateien
        for file_path in desktop_dir.iterdir():
            if file_path.is_file():
                file_ext = file_path.suffix.lower()
                
                # Finde passende Kategorie
                target_category = None
                for category, extensions in self.file_categories.items():
                    if file_ext in extensions:
                        target_category = category
                        break
                
                if target_category:
                    try:
                        if not dry_run:
                            destination = desktop_dir / target_category / file_path.name
                            shutil.move(str(file_path), str(destination))
                        
                        organized_count += 1
                        
                    except Exception as e:
                        print(f"⚠️ Fehler beim Organisieren {file_path}: {e}")
        
        return {
            'success': True,
            'action': 'organize_desktop',
            'organized_files': organized_count
        }
    
    def create_backup_important_files(self, backup_location: Optional[str] = None) -> Dict:
        """Erstellt Backup wichtiger Dateien vor Aufräumung"""
        if not backup_location:
            backup_location = os.path.expanduser("~/Toobix_Backup")
        
        backup_dir = Path(backup_location)
        backup_dir.mkdir(exist_ok=True)
        
        important_dirs = [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Pictures")
        ]
        
        backup_info = {
            'backup_location': str(backup_dir),
            'backed_up_dirs': [],
            'total_size_gb': 0
        }
        
        print("💾 Erstelle Sicherheitskopie wichtiger Dateien...")
        
        for source_dir in important_dirs:
            if os.path.exists(source_dir):
                dir_name = os.path.basename(source_dir)
                backup_target = backup_dir / f"{dir_name}_{datetime.datetime.now().strftime('%Y%m%d')}"
                
                try:
                    shutil.copytree(source_dir, backup_target, dirs_exist_ok=True)
                    
                    # Größe berechnen
                    size = sum(f.stat().st_size for f in backup_target.rglob('*') if f.is_file())
                    size_gb = size / (1024**3)
                    
                    backup_info['backed_up_dirs'].append({
                        'source': source_dir,
                        'backup': str(backup_target),
                        'size_gb': round(size_gb, 2)
                    })
                    backup_info['total_size_gb'] += size_gb
                    
                except Exception as e:
                    print(f"⚠️ Fehler beim Backup von {source_dir}: {e}")
        
        return backup_info
