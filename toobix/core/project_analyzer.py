"""
Toobix Project Analyzer
Findet und organisiert Code-Projekte, Snippets und angefangene Programme
"""
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import hashlib

class ProjectAnalyzer:
    """Intelligente Projekt- und Code-Analyse"""
    
    def __init__(self, settings):
        self.settings = settings
        
        # Code-Dateierweiterungen
        self.code_extensions = {
            'Python': ['.py', '.pyw', '.ipynb'],
            'JavaScript': ['.js', '.jsx', '.ts', '.tsx', '.vue'],
            'Web': ['.html', '.htm', '.css', '.scss', '.sass'],
            'C/C++': ['.c', '.cpp', '.cc', '.cxx', '.h', '.hpp'],
            'Java': ['.java', '.jar'],
            'C#': ['.cs', '.csx'],
            'PHP': ['.php', '.phtml'],
            'Go': ['.go'],
            'Rust': ['.rs'],
            'Ruby': ['.rb'],
            'PowerShell': ['.ps1', '.psm1'],
            'Batch': ['.bat', '.cmd'],
            'SQL': ['.sql'],
            'XML/Config': ['.xml', '.json', '.yaml', '.yml', '.toml', '.ini'],
            'Markdown': ['.md', '.markdown'],
            'R': ['.r', '.R'],
            'Matlab': ['.m'],
            'Lua': ['.lua']
        }
        
        # Projekt-Indikatoren (Dateien die auf Projekte hinweisen)
        self.project_indicators = {
            'Python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', '__init__.py'],
            'Node.js': ['package.json', 'package-lock.json', 'yarn.lock', 'node_modules/'],
            'Web': ['index.html', 'webpack.config.js', 'gulpfile.js'],
            'C/C++': ['Makefile', 'CMakeLists.txt', '*.vcxproj'],
            'Java': ['pom.xml', 'build.gradle', 'build.xml'],
            'C#': ['*.csproj', '*.sln', 'packages.config'],
            'Git': ['.git/', '.gitignore', 'README.md'],
            'Docker': ['Dockerfile', 'docker-compose.yml'],
            'Database': ['*.db', '*.sqlite', '*.sql']
        }
        
        # Verzeichnisse die normalerweise Projekte enthalten
        self.common_project_dirs = [
            "~/Documents",
            "~/Desktop", 
            "~/Downloads",
            "~/Projects",
            "~/Code",
            "~/Development",
            "~/Workspace",
            "C:/Development",
            "C:/Projects",
            "C:/Code"
        ]
        
        print("🔍 Project Analyzer initialisiert")
    
    def scan_for_projects(self, deep_scan: bool = False) -> Dict:
        """Scannt das System nach Code-Projekten und Snippets"""
        print("🔍 Scanne nach Code-Projekten...")
        
        results = {
            'complete_projects': [],
            'code_snippets': [],
            'abandoned_projects': [],
            'project_suggestions': [],
            'duplicate_projects': [],
            'total_files_scanned': 0,
            'scan_summary': {}
        }
        
        scan_dirs = [os.path.expanduser(d) for d in self.common_project_dirs if os.path.exists(os.path.expanduser(d))]
        
        for scan_dir in scan_dirs:
            print(f"📁 Scanne: {scan_dir}")
            
            try:
                for root, dirs, files in os.walk(scan_dir):
                    # Skip versteckte und System-Ordner
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.venv']]
                    
                    if deep_scan or len(root.split(os.sep)) <= len(scan_dir.split(os.sep)) + 3:
                        project_info = self._analyze_directory(root, files)
                        if project_info:
                            # Kategorisiere Projekt
                            if project_info['project_score'] >= 8:
                                results['complete_projects'].append(project_info)
                            elif project_info['project_score'] >= 4:
                                results['abandoned_projects'].append(project_info)
                            elif project_info['code_files'] > 0:
                                results['code_snippets'].append(project_info)
                    
                    results['total_files_scanned'] += len(files)
                    
            except Exception as e:
                print(f"⚠️ Fehler beim Scannen von {scan_dir}: {e}")
        
        # Duplikate finden
        results['duplicate_projects'] = self._find_duplicate_projects(
            results['complete_projects'] + results['abandoned_projects']
        )
        
        # Organisationsvorschläge
        results['project_suggestions'] = self._generate_project_suggestions(results)
        
        # Zusammenfassung
        results['scan_summary'] = self._create_scan_summary(results)
        
        print(f"✅ Scan abgeschlossen: {results['total_files_scanned']} Dateien analysiert")
        return results
    
    def _analyze_directory(self, directory: str, files: List[str]) -> Optional[Dict]:
        """Analysiert ein Verzeichnis auf Projekt-Eigenschaften"""
        dir_path = Path(directory)
        
        # Skip zu tiefe oder irrelevante Verzeichnisse
        if len(str(dir_path).split(os.sep)) > 10:
            return None
        
        code_files = []
        project_files = []
        project_type = "Unknown"
        project_score = 0
        
        # Analysiere Dateien
        for file in files:
            file_path = dir_path / file
            if not file_path.exists():
                continue
                
            file_ext = file_path.suffix.lower()
            
            # Code-Dateien identifizieren
            for lang, extensions in self.code_extensions.items():
                if file_ext in extensions:
                    code_files.append({
                        'name': file,
                        'language': lang,
                        'size': file_path.stat().st_size if file_path.exists() else 0,
                        'lines': self._count_lines(file_path)
                    })
                    project_score += 1
                    break
            
            # Projekt-Indikatoren
            for proj_type, indicators in self.project_indicators.items():
                if any(indicator in file for indicator in indicators):
                    project_files.append(file)
                    project_type = proj_type
                    project_score += 3
        
        # Verzeichnis-basierte Indikatoren
        subdirs = [d for d in dir_path.iterdir() if d.is_dir()]
        for subdir in subdirs:
            if subdir.name in ['.git', '.svn', 'node_modules', '.vscode', '.idea']:
                project_score += 2
                project_files.append(subdir.name + '/')
        
        # Nur relevante Verzeichnisse zurückgeben
        if project_score < 2 and len(code_files) < 3:
            return None
        
        # Projekt-Zustand bewerten
        status = "active"
        last_modified = max([f.stat().st_mtime for f in dir_path.iterdir() if f.is_file()], default=0)
        days_since_modified = (time.time() - last_modified) / (24 * 3600) if last_modified else 999
        
        if days_since_modified > 90:
            status = "abandoned"
        elif days_since_modified > 30:
            status = "stale"
        
        return {
            'path': str(directory),
            'name': dir_path.name,
            'project_type': project_type,
            'project_score': project_score,
            'status': status,
            'code_files': len(code_files),
            'code_details': code_files[:10],  # Begrenzt auf 10 für Performance
            'project_files': project_files,
            'total_lines': sum(f['lines'] for f in code_files),
            'languages': list(set(f['language'] for f in code_files)),
            'last_modified_days': int(days_since_modified),
            'estimated_size_mb': sum(f['size'] for f in code_files) / (1024*1024)
        }
    
    def _count_lines(self, file_path: Path) -> int:
        """Zählt Zeilen in einer Code-Datei"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for line in f if line.strip())
        except:
            return 0
    
    def _find_duplicate_projects(self, projects: List[Dict]) -> List[Dict]:
        """Findet potentielle Duplikate von Projekten"""
        duplicates = []
        seen_names = defaultdict(list)
        
        for project in projects:
            # Normalisierter Name für Vergleich
            normalized_name = re.sub(r'[_\-\s]+', '', project['name'].lower())
            seen_names[normalized_name].append(project)
        
        for name, project_list in seen_names.items():
            if len(project_list) > 1:
                duplicates.append({
                    'name': name,
                    'projects': project_list,
                    'suggestion': 'Prüfe ob diese Projekte zusammengehören oder Duplikate sind'
                })
        
        return duplicates
    
    def _generate_project_suggestions(self, scan_results: Dict) -> List[Dict]:
        """Generiert Organisationsvorschläge für Projekte"""
        suggestions = []
        
        # Vorschlag 1: Projekt-Verzeichnis erstellen
        if scan_results['complete_projects'] or scan_results['abandoned_projects']:
            suggestions.append({
                'type': 'create_project_structure',
                'title': 'Projekt-Verzeichnis-Struktur erstellen',
                'description': 'Erstelle eine organisierte Struktur: ~/Projects/Active/, ~/Projects/Archive/, ~/Projects/Snippets/',
                'priority': 'high',
                'estimated_time': '5 Minuten'
            })
        
        # Vorschlag 2: Verlassene Projekte archivieren
        abandoned = [p for p in scan_results['abandoned_projects'] if p['last_modified_days'] > 180]
        if abandoned:
            suggestions.append({
                'type': 'archive_old_projects',
                'title': f'{len(abandoned)} alte Projekte archivieren',
                'description': f'Verschiebe {len(abandoned)} Projekte die >6 Monate nicht bearbeitet wurden',
                'priority': 'medium',
                'projects': abandoned
            })
        
        # Vorschlag 3: Code-Snippets organisieren
        if len(scan_results['code_snippets']) > 10:
            suggestions.append({
                'type': 'organize_snippets',
                'title': f'{len(scan_results["code_snippets"])} Code-Snippets organisieren',
                'description': 'Sammle einzelne Code-Dateien in einem Snippets-Ordner nach Sprache sortiert',
                'priority': 'low',
                'snippets': scan_results['code_snippets'][:20]
            })
        
        # Vorschlag 4: Git-Repositories initialisieren
        ungit_projects = [p for p in scan_results['complete_projects'] if '.git/' not in p['project_files']]
        if ungit_projects:
            suggestions.append({
                'type': 'init_git_repos',
                'title': f'{len(ungit_projects)} Projekte haben kein Git',
                'description': 'Initialisiere Git-Repositories für bessere Versionskontrolle',
                'priority': 'low',
                'projects': ungit_projects[:10]
            })
        
        return suggestions
    
    def _create_scan_summary(self, results: Dict) -> Dict:
        """Erstellt Zusammenfassung des Scans"""
        total_projects = len(results['complete_projects']) + len(results['abandoned_projects'])
        total_code_files = sum(p['code_files'] for p in results['complete_projects'] + results['abandoned_projects'] + results['code_snippets'])
        total_lines = sum(p['total_lines'] for p in results['complete_projects'] + results['abandoned_projects'] + results['code_snippets'])
        
        # Sprachen-Statistik
        language_stats = defaultdict(int)
        for project in results['complete_projects'] + results['abandoned_projects'] + results['code_snippets']:
            for lang in project['languages']:
                language_stats[lang] += project['code_files']
        
        return {
            'total_projects': total_projects,
            'active_projects': len(results['complete_projects']),
            'abandoned_projects': len(results['abandoned_projects']),
            'code_snippets': len(results['code_snippets']),
            'total_code_files': total_code_files,
            'total_lines_of_code': total_lines,
            'most_used_languages': sorted(language_stats.items(), key=lambda x: x[1], reverse=True)[:5],
            'duplicate_sets': len(results['duplicate_projects']),
            'suggestions_count': len(results['project_suggestions'])
        }
    
    def create_project_organization_plan(self, scan_results: Dict) -> Dict:
        """Erstellt detaillierten Organisationsplan"""
        plan = {
            'target_structure': self._design_project_structure(),
            'migration_steps': [],
            'estimated_time': 0,
            'safety_checks': [],
            'benefits': []
        }
        
        # Migration Steps generieren
        if scan_results['complete_projects']:
            plan['migration_steps'].append({
                'step': 1,
                'action': 'Erstelle Projekt-Verzeichnisse',
                'description': 'Erstelle ~/Projects/{Active,Archive,Snippets,Learning}',
                'time_minutes': 2
            })
            
            plan['migration_steps'].append({
                'step': 2,
                'action': f'Verschiebe {len(scan_results["complete_projects"])} aktive Projekte',
                'description': 'Aktive Projekte nach ~/Projects/Active/',
                'time_minutes': len(scan_results['complete_projects']) * 2
            })
        
        if scan_results['abandoned_projects']:
            plan['migration_steps'].append({
                'step': 3,
                'action': f'Archiviere {len(scan_results["abandoned_projects"])} alte Projekte',
                'description': 'Alte Projekte nach ~/Projects/Archive/',
                'time_minutes': len(scan_results['abandoned_projects'])
            })
        
        if scan_results['code_snippets']:
            plan['migration_steps'].append({
                'step': 4,
                'action': f'Organisiere {len(scan_results["code_snippets"])} Code-Snippets',
                'description': 'Snippets nach Sprache in ~/Projects/Snippets/ sortieren',
                'time_minutes': len(scan_results['code_snippets']) // 2
            })
        
        plan['estimated_time'] = sum(step['time_minutes'] for step in plan['migration_steps'])
        
        # Sicherheitsmaßnahmen
        plan['safety_checks'] = [
            'Backup aller Projekte vor Migration',
            'Git-Status prüfen bei versionierten Projekten',
            'Symbolische Links beibehalten',
            'IDE-Konfigurationen anpassen',
            'PATH-Variablen aktualisieren'
        ]
        
        # Vorteile
        plan['benefits'] = [
            'Klare Projekt-Struktur',
            'Einfachere Projekt-Suche',
            'Bessere Backup-Strategien',
            'Reduzierte Duplikate',
            'Professionellere Entwicklungsumgebung'
        ]
        
        return plan
    
    def _design_project_structure(self) -> Dict:
        """Entwirft optimale Projekt-Struktur"""
        return {
            'base_path': '~/Projects',
            'subdirectories': {
                'Active': 'Aktuell entwickelte Projekte',
                'Archive': 'Abgeschlossene oder eingefrorene Projekte', 
                'Snippets': 'Code-Schnipsel und Experimente',
                'Learning': 'Tutorials und Lernprojekte',
                'Templates': 'Projekt-Vorlagen und Boilerplate',
                'Collaboration': 'Gemeinsame oder Open-Source Projekte'
            },
            'naming_convention': 'lowercase-with-dashes',
            'readme_template': True,
            'git_integration': True
        }

import time
