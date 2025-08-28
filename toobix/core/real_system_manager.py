"""
TOOBIX - Real System Manager
Echte System-Analyse und -Verwaltung ohne Halluzinationen
"""

import psutil
import os
import subprocess
import time
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import tempfile
import json

class RealSystemManager:
    """Echte System-Verwaltung ohne KI-Halluzinationen"""
    
    def __init__(self):
        self.last_scan_time = 0
        self.process_cache = {}
        
    def get_real_ram_usage(self) -> Dict:
        """Echte RAM-Nutzung ohne Erfindungen"""
        try:
            memory = psutil.virtual_memory()
            processes = []
            
            # Top 10 RAM-Verbraucher ECHT ermitteln
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    proc_info = proc.info
                    if proc_info['memory_info']:
                        memory_mb = proc_info['memory_info'].rss / (1024 * 1024)
                        if memory_mb > 50:  # Nur >50MB anzeigen
                            processes.append({
                                'pid': proc_info['pid'],
                                'name': proc_info['name'],
                                'memory_mb': memory_mb,
                                'memory_percent': (proc_info['memory_info'].rss / memory.total) * 100
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Nach RAM-Verbrauch sortieren
            processes.sort(key=lambda x: x['memory_mb'], reverse=True)
            
            return {
                'total_gb': memory.total / (1024**3),
                'used_gb': memory.used / (1024**3),
                'available_gb': memory.available / (1024**3),
                'percent': memory.percent,
                'top_processes': processes[:10]
            }
        except Exception as e:
            return {'error': f"Fehler bei RAM-Analyse: {e}"}
    
    def kill_process_real(self, process_name: str) -> Dict:
        """Echtes Beenden von Prozessen"""
        killed_count = 0
        errors = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'].lower() == process_name.lower():
                        proc.terminate()
                        killed_count += 1
                        time.sleep(0.1)  # Kurz warten
                        
                        # Falls nötig: Force kill
                        if proc.is_running():
                            proc.kill()
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                    errors.append(f"Fehler bei PID {proc.info['pid']}: {e}")
                    
        except Exception as e:
            return {'success': False, 'error': f"Kritischer Fehler: {e}"}
        
        return {
            'success': True,
            'killed_count': killed_count,
            'errors': errors
        }
    
    def find_large_files_real(self, min_size_mb: int = 100) -> List[Dict]:
        """Echte große Dateien finden"""
        large_files = []
        
        # Standard-Ordner scannen
        scan_paths = [
            Path.home() / 'Downloads',
            Path.home() / 'Documents', 
            Path.home() / 'Desktop',
            Path.home() / 'Pictures',
            Path.home() / 'Videos'
        ]
        
        for scan_path in scan_paths:
            if not scan_path.exists():
                continue
                
            try:
                for file_path in scan_path.rglob('*'):
                    try:
                        if file_path.is_file():
                            size_bytes = file_path.stat().st_size
                            size_mb = size_bytes / (1024 * 1024)
                            
                            if size_mb >= min_size_mb:
                                large_files.append({
                                    'path': str(file_path),
                                    'name': file_path.name,
                                    'size_mb': size_mb,
                                    'size_gb': size_bytes / (1024**3),
                                    'extension': file_path.suffix.lower(),
                                    'parent_dir': str(file_path.parent)
                                })
                    except (PermissionError, OSError, FileNotFoundError):
                        continue
                        
            except (PermissionError, OSError):
                continue
        
        # Nach Größe sortieren
        large_files.sort(key=lambda x: x['size_mb'], reverse=True)
        return large_files
    
    def organize_files_real(self, source_dir: str) -> Dict:
        """Echte Datei-Organisation"""
        source_path = Path(source_dir)
        if not source_path.exists():
            return {'success': False, 'error': 'Quell-Ordner existiert nicht'}
        
        # Basis-Organisationsstruktur
        org_base = Path.home() / 'TOOBIX_ORGANISATION'
        org_base.mkdir(exist_ok=True)
        
        # Kategorie-Ordner
        categories = {
            'documents': org_base / '01_DOKUMENTE',
            'images': org_base / '02_BILDER', 
            'videos': org_base / '03_VIDEOS',
            'audio': org_base / '04_AUDIO',
            'archives': org_base / '05_ARCHIVE',
            'programs': org_base / '06_PROGRAMME',
            'other': org_base / '99_SONSTIGES'
        }
        
        # Ordner erstellen
        for cat_path in categories.values():
            cat_path.mkdir(exist_ok=True)
        
        # Datei-Erweiterungen zuordnen
        extensions_map = {
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx'],
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'],
            'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
            'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
            'programs': ['.exe', '.msi', '.deb', '.rpm', '.dmg', '.app']
        }
        
        moved_files = []
        errors = []
        
        try:
            for file_path in source_path.iterdir():
                if file_path.is_file():
                    file_ext = file_path.suffix.lower()
                    
                    # Kategorie bestimmen
                    target_category = 'other'
                    for category, extensions in extensions_map.items():
                        if file_ext in extensions:
                            target_category = category
                            break
                    
                    # Ziel-Pfad
                    target_dir = categories[target_category]
                    target_path = target_dir / file_path.name
                    
                    # Duplikate vermeiden
                    counter = 1
                    original_target = target_path
                    while target_path.exists():
                        stem = original_target.stem
                        suffix = original_target.suffix
                        target_path = target_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                    
                    try:
                        shutil.move(str(file_path), str(target_path))
                        moved_files.append({
                            'source': str(file_path),
                            'target': str(target_path),
                            'category': target_category
                        })
                    except Exception as e:
                        errors.append(f"Fehler bei {file_path.name}: {e}")
                        
        except Exception as e:
            return {'success': False, 'error': f"Kritischer Fehler: {e}"}
        
        return {
            'success': True,
            'moved_files': len(moved_files),
            'errors': len(errors),
            'details': moved_files,
            'error_details': errors,
            'organization_path': str(org_base)
        }
    
    def clean_temp_files_real(self) -> Dict:
        """Echte Temp-Dateien löschen"""
        deleted_files = 0
        deleted_size = 0
        errors = []
        
        temp_paths = [
            Path(tempfile.gettempdir()),
            Path(os.environ.get('LOCALAPPDATA', '')) / 'Temp',
            Path('C:/Windows/Temp')
        ]
        
        for temp_path in temp_paths:
            if not temp_path.exists():
                continue
                
            try:
                for item in temp_path.iterdir():
                    try:
                        if item.is_file():
                            size = item.stat().st_size
                            item.unlink()
                            deleted_files += 1
                            deleted_size += size
                        elif item.is_dir():
                            shutil.rmtree(item)
                            deleted_files += 1
                    except (PermissionError, FileNotFoundError, OSError) as e:
                        errors.append(f"Fehler bei {item.name}: {e}")
                        
            except (PermissionError, OSError) as e:
                errors.append(f"Fehler bei Temp-Ordner {temp_path}: {e}")
        
        return {
            'deleted_files': deleted_files,
            'deleted_size_mb': deleted_size / (1024 * 1024),
            'errors': len(errors),
            'error_details': errors[:5]  # Nur erste 5 Fehler anzeigen
        }
    
    def get_running_programs_real(self) -> List[Dict]:
        """Echte laufende Programme ermitteln"""
        programs = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe', 'memory_info', 'cpu_percent']):
            try:
                proc_info = proc.info
                if proc_info['exe'] and proc_info['memory_info']:
                    programs.append({
                        'pid': proc_info['pid'],
                        'name': proc_info['name'],
                        'exe_path': proc_info['exe'],
                        'memory_mb': proc_info['memory_info'].rss / (1024 * 1024),
                        'cpu_percent': proc.cpu_percent()
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Nach Speicherverbrauch sortieren
        programs.sort(key=lambda x: x['memory_mb'], reverse=True)
        return programs
    
    def create_system_report(self) -> Dict:
        """Umfassender System-Bericht"""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'ram_usage': self.get_real_ram_usage(),
            'large_files': self.find_large_files_real(),
            'running_programs': self.get_running_programs_real()[:20],  # Top 20
            'disk_usage': {}
        }
        
        # Festplatten-Info
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                report['disk_usage'][partition.device] = {
                    'total_gb': usage.total / (1024**3),
                    'used_gb': usage.used / (1024**3),
                    'free_gb': usage.free / (1024**3),
                    'percent': (usage.used / usage.total) * 100
                }
            except PermissionError:
                continue
        
        return report
