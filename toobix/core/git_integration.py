"""
Toobix Git Integration
Umfassendes Git-Repository-Management und Automatisierung
"""
import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import shutil

class GitManager:
    """Intelligentes Git-Repository-Management für Toobix"""
    
    def __init__(self, settings=None):
        self.settings = settings
        self.git_command = "git"
        
        # Teste Git-Verfügbarkeit
        self.git_available = self._check_git_availability()
        if self.git_available:
            print("🔧 Git Integration initialisiert")
        else:
            print("⚠️ Git nicht verfügbar - Git-Features deaktiviert")
    
    def _check_git_availability(self) -> bool:
        """Prüft ob Git installiert und verfügbar ist"""
        try:
            result = subprocess.run([self.git_command, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def scan_git_repositories(self, scan_dirs: List[str] = None) -> List[Dict[str, Any]]:
        """Scannt nach Git-Repositories im System"""
        if not self.git_available:
            return []
        
        if not scan_dirs:
            # Standard-Scan-Verzeichnisse
            user_home = Path.home()
            scan_dirs = [
                str(user_home / "Documents"),
                str(user_home / "Desktop"),
                str(user_home / "Projects"),
                str(user_home / "source"),
                "C:\\Projects",
                "C:\\dev",
                "C:\\Source"
            ]
        
        repositories = []
        
        for scan_dir in scan_dirs:
            if not os.path.exists(scan_dir):
                continue
                
            try:
                for root, dirs, files in os.walk(scan_dir):
                    if '.git' in dirs:
                        repo_info = self._analyze_repository(root)
                        if repo_info:
                            repositories.append(repo_info)
                        
                        # Skip .git Unterverzeichnisse
                        dirs.remove('.git')
            except PermissionError:
                continue
        
        return sorted(repositories, key=lambda x: x.get('last_commit_date', ''), reverse=True)
    
    def _analyze_repository(self, repo_path: str) -> Optional[Dict[str, Any]]:
        """Analysiert ein Git-Repository detailliert"""
        try:
            repo_info = {
                'path': repo_path,
                'name': os.path.basename(repo_path),
                'status': 'unknown',
                'branch': None,
                'commits_ahead': 0,
                'commits_behind': 0,
                'uncommitted_changes': False,
                'untracked_files': [],
                'last_commit_date': None,
                'last_commit_message': None,
                'remote_url': None,
                'size_mb': 0,
                'file_count': 0,
                'language': 'unknown'
            }
            
            # Wechsle ins Repository-Verzeichnis
            original_cwd = os.getcwd()
            os.chdir(repo_path)
            
            try:
                # Branch-Information
                result = subprocess.run([self.git_command, "branch", "--show-current"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    repo_info['branch'] = result.stdout.strip()
                
                # Remote-URL
                result = subprocess.run([self.git_command, "remote", "get-url", "origin"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    repo_info['remote_url'] = result.stdout.strip()
                
                # Status-Check
                result = subprocess.run([self.git_command, "status", "--porcelain"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
                    repo_info['uncommitted_changes'] = len(status_lines) > 0
                    repo_info['untracked_files'] = [line[3:] for line in status_lines if line.startswith('??')]
                
                # Letzter Commit
                result = subprocess.run([self.git_command, "log", "-1", "--format=%cd|%s", "--date=iso"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0 and result.stdout.strip():
                    date_msg = result.stdout.strip().split('|', 1)
                    if len(date_msg) == 2:
                        repo_info['last_commit_date'] = date_msg[0].strip()
                        repo_info['last_commit_message'] = date_msg[1].strip()
                
                # Remote-Tracking-Status
                if repo_info['remote_url']:
                    result = subprocess.run([self.git_command, "rev-list", "--count", "--left-right", "HEAD...origin/" + (repo_info['branch'] or 'main')], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0 and result.stdout.strip():
                        counts = result.stdout.strip().split('\t')
                        if len(counts) == 2:
                            repo_info['commits_ahead'] = int(counts[0])
                            repo_info['commits_behind'] = int(counts[1])
                
                # Repository-Größe und Datei-Count
                repo_size = 0
                file_count = 0
                for root, dirs, files in os.walk(repo_path):
                    # Skip .git Verzeichnis für genaue Größe
                    if '.git' in root:
                        continue
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            repo_size += os.path.getsize(file_path)
                            file_count += 1
                        except (OSError, PermissionError):
                            continue
                
                repo_info['size_mb'] = round(repo_size / (1024 * 1024), 2)
                repo_info['file_count'] = file_count
                
                # Programmiersprache erkennen
                repo_info['language'] = self._detect_repository_language(repo_path)
                
                # Status bestimmen
                if repo_info['uncommitted_changes']:
                    repo_info['status'] = 'dirty'
                elif repo_info['commits_ahead'] > 0:
                    repo_info['status'] = 'ahead'
                elif repo_info['commits_behind'] > 0:
                    repo_info['status'] = 'behind'
                else:
                    repo_info['status'] = 'clean'
                
            finally:
                os.chdir(original_cwd)
            
            return repo_info
            
        except Exception as e:
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
            print(f"Fehler bei Repository-Analyse {repo_path}: {e}")
            return None
    
    def _detect_repository_language(self, repo_path: str) -> str:
        """Erkennt die Hauptprogrammiersprache eines Repositories"""
        language_files = {
            'python': ['.py', 'requirements.txt', 'setup.py', 'pyproject.toml'],
            'javascript': ['package.json', '.js', '.ts', '.jsx', '.tsx'],
            'java': ['.java', 'pom.xml', 'build.gradle'],
            'csharp': ['.cs', '.csproj', '.sln'],
            'cpp': ['.cpp', '.hpp', '.h', '.cc', 'CMakeLists.txt'],
            'go': ['.go', 'go.mod'],
            'rust': ['.rs', 'Cargo.toml'],
            'php': ['.php', 'composer.json'],
            'ruby': ['.rb', 'Gemfile'],
            'swift': ['.swift', 'Package.swift']
        }
        
        file_counts = {lang: 0 for lang in language_files.keys()}
        
        try:
            for root, dirs, files in os.walk(repo_path):
                if '.git' in root:
                    continue
                    
                for file in files:
                    file_lower = file.lower()
                    file_ext = os.path.splitext(file)[1]
                    
                    for lang, patterns in language_files.items():
                        for pattern in patterns:
                            if pattern.startswith('.') and file_ext == pattern:
                                file_counts[lang] += 1
                            elif file_lower == pattern.lower():
                                file_counts[lang] += 5  # Config-Dateien höher gewichten
        except:
            pass
        
        # Finde dominante Sprache
        max_count = max(file_counts.values())
        if max_count > 0:
            for lang, count in file_counts.items():
                if count == max_count:
                    return lang
        
        return 'mixed'
    
    def get_repository_status(self, repo_path: str) -> str:
        """Gibt detaillierten Status eines Repositories zurück"""
        if not self.git_available:
            return "❌ Git nicht verfügbar"
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return f"❌ '{repo_path}' ist kein Git-Repository"
        
        repo_info = self._analyze_repository(repo_path)
        if not repo_info:
            return f"❌ Fehler bei der Analyse von '{repo_path}'"
        
        status_report = f"📁 GIT-REPOSITORY STATUS\n"
        status_report += f"Pfad: {repo_info['path']}\n"
        status_report += f"Name: {repo_info['name']}\n"
        status_report += f"Branch: {repo_info['branch'] or 'unbekannt'}\n"
        status_report += f"Sprache: {repo_info['language']}\n"
        status_report += f"Größe: {repo_info['size_mb']} MB ({repo_info['file_count']} Dateien)\n\n"
        
        # Status-Icons
        status_icons = {
            'clean': '✅',
            'dirty': '⚠️',
            'ahead': '⬆️',
            'behind': '⬇️'
        }
        
        status_report += f"Status: {status_icons.get(repo_info['status'], '❓')} {repo_info['status']}\n"
        
        if repo_info['uncommitted_changes']:
            status_report += f"⚠️ Uncommitted Changes vorhanden\n"
        
        if repo_info['untracked_files']:
            status_report += f"📄 {len(repo_info['untracked_files'])} untracked Dateien\n"
        
        if repo_info['commits_ahead'] > 0:
            status_report += f"⬆️ {repo_info['commits_ahead']} Commits ahead of remote\n"
        
        if repo_info['commits_behind'] > 0:
            status_report += f"⬇️ {repo_info['commits_behind']} Commits behind remote\n"
        
        if repo_info['last_commit_date']:
            status_report += f"\nLetzter Commit: {repo_info['last_commit_date']}\n"
            if repo_info['last_commit_message']:
                status_report += f"Message: {repo_info['last_commit_message']}\n"
        
        if repo_info['remote_url']:
            status_report += f"\nRemote: {repo_info['remote_url']}\n"
        
        return status_report
    
    def auto_commit_push(self, repo_path: str, message: str = None) -> str:
        """Automatisches Commit und Push"""
        if not self.git_available:
            return "❌ Git nicht verfügbar"
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return f"❌ '{repo_path}' ist kein Git-Repository"
        
        original_cwd = os.getcwd()
        
        try:
            os.chdir(repo_path)
            
            # Check für uncommitted changes
            result = subprocess.run([self.git_command, "status", "--porcelain"], 
                                  capture_output=True, text=True, timeout=10)
            
            if not result.stdout.strip():
                return "✅ Keine Änderungen zum Committen"
            
            # Add all changes
            result = subprocess.run([self.git_command, "add", "."], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return f"❌ Fehler beim Git Add: {result.stderr}"
            
            # Commit
            if not message:
                message = f"Auto-commit via Toobix - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            result = subprocess.run([self.git_command, "commit", "-m", message], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return f"❌ Fehler beim Commit: {result.stderr}"
            
            # Push (falls remote existiert)
            result = subprocess.run([self.git_command, "remote"], 
                                  capture_output=True, text=True, timeout=10)
            if result.stdout.strip():
                push_result = subprocess.run([self.git_command, "push"], 
                                           capture_output=True, text=True, timeout=60)
                if push_result.returncode == 0:
                    return f"✅ Erfolgreich committed und gepusht: '{message}'"
                else:
                    return f"⚠️ Committed, aber Push fehlgeschlagen: {push_result.stderr}"
            else:
                return f"✅ Erfolgreich committed (kein Remote): '{message}'"
        
        except Exception as e:
            return f"❌ Fehler beim Auto-Commit: {e}"
        
        finally:
            os.chdir(original_cwd)
    
    def pull_latest(self, repo_path: str) -> str:
        """Pullt neueste Änderungen vom Remote"""
        if not self.git_available:
            return "❌ Git nicht verfügbar"
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return f"❌ '{repo_path}' ist kein Git-Repository"
        
        original_cwd = os.getcwd()
        
        try:
            os.chdir(repo_path)
            
            # Check für Remote
            result = subprocess.run([self.git_command, "remote"], 
                                  capture_output=True, text=True, timeout=10)
            if not result.stdout.strip():
                return "❌ Kein Remote-Repository konfiguriert"
            
            # Pull
            result = subprocess.run([self.git_command, "pull"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                if "Already up to date" in result.stdout:
                    return "✅ Repository ist bereits aktuell"
                else:
                    return f"✅ Erfolgreich gepullt:\n{result.stdout}"
            else:
                return f"❌ Pull fehlgeschlagen: {result.stderr}"
        
        except Exception as e:
            return f"❌ Fehler beim Pull: {e}"
        
        finally:
            os.chdir(original_cwd)
    
    def create_repository_report(self) -> str:
        """Erstellt umfassenden Bericht über alle Git-Repositories"""
        if not self.git_available:
            return "❌ Git nicht verfügbar - Repository-Report nicht möglich"
        
        repositories = self.scan_git_repositories()
        
        if not repositories:
            return "📂 Keine Git-Repositories gefunden"
        
        report = f"📊 GIT-REPOSITORY-BERICHT\n"
        report += f"{'='*50}\n\n"
        report += f"🔍 {len(repositories)} Repositories gefunden\n\n"
        
        # Gruppiere nach Status
        status_groups = {
            'clean': [],
            'dirty': [],
            'ahead': [],
            'behind': [],
            'unknown': []
        }
        
        languages = {}
        total_size = 0
        
        for repo in repositories:
            status_groups[repo['status']].append(repo)
            
            # Sprachen-Statistik
            lang = repo['language']
            languages[lang] = languages.get(lang, 0) + 1
            
            total_size += repo['size_mb']
        
        # Status-Übersicht
        report += "📋 STATUS-ÜBERSICHT:\n"
        for status, repos in status_groups.items():
            if repos:
                icon = {'clean': '✅', 'dirty': '⚠️', 'ahead': '⬆️', 'behind': '⬇️', 'unknown': '❓'}[status]
                report += f"{icon} {status.title()}: {len(repos)} Repositories\n"
        report += "\n"
        
        # Sprachen-Verteilung
        if languages:
            report += "🔧 SPRACHEN-VERTEILUNG:\n"
            for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                report += f"• {lang}: {count} Repository(s)\n"
            report += "\n"
        
        # Größen-Info
        report += f"💾 GESAMT-GRÖSSE: {total_size:.1f} MB\n\n"
        
        # Problematische Repositories
        dirty_repos = status_groups['dirty']
        if dirty_repos:
            report += "⚠️ REPOSITORIES MIT UNCOMMITTED CHANGES:\n"
            for repo in dirty_repos:
                report += f"• {repo['name']} ({repo['path']})\n"
                if repo['untracked_files']:
                    report += f"  📄 {len(repo['untracked_files'])} untracked Dateien\n"
            report += "\n"
        
        # Repositories die ahead/behind sind
        sync_issues = status_groups['ahead'] + status_groups['behind']
        if sync_issues:
            report += "🔄 REPOSITORIES MIT SYNC-PROBLEMEN:\n"
            for repo in sync_issues:
                ahead = repo['commits_ahead']
                behind = repo['commits_behind']
                sync_status = f"⬆️{ahead} ⬇️{behind}" if ahead and behind else f"⬆️{ahead}" if ahead else f"⬇️{behind}"
                report += f"• {repo['name']}: {sync_status}\n"
            report += "\n"
        
        # Aktivste Repositories (nach letztem Commit)
        report += "⏰ LETZTE AKTIVITÄT:\n"
        active_repos = [r for r in repositories if r['last_commit_date']][:5]
        for repo in active_repos:
            report += f"• {repo['name']}: {repo['last_commit_date']}\n"
        
        report += f"\n📅 Erstellt: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        
        return report
    
    def repository_health_check(self) -> Dict[str, Any]:
        """Führt Gesundheitscheck für alle Repositories durch"""
        if not self.git_available:
            return {'status': 'error', 'message': 'Git nicht verfügbar'}
        
        repositories = self.scan_git_repositories()
        
        issues = []
        recommendations = []
        
        dirty_count = len([r for r in repositories if r['status'] == 'dirty'])
        ahead_count = len([r for r in repositories if r['commits_ahead'] > 0])
        behind_count = len([r for r in repositories if r['commits_behind'] > 0])
        
        if dirty_count > 0:
            issues.append(f"⚠️ {dirty_count} Repository(s) haben uncommitted changes")
            recommendations.append("Committe oder stash deine Änderungen")
        
        if ahead_count > 0:
            issues.append(f"⬆️ {ahead_count} Repository(s) sind ahead of remote")
            recommendations.append("Pushe deine lokalen Commits")
        
        if behind_count > 0:
            issues.append(f"⬇️ {behind_count} Repository(s) sind behind remote")
            recommendations.append("Pulle die neuesten Änderungen")
        
        # Gesamtstatus
        if not issues:
            status = 'excellent'
        elif len(issues) <= 2:
            status = 'good'
        else:
            status = 'needs_attention'
        
        return {
            'status': status,
            'total_repositories': len(repositories),
            'issues': issues,
            'recommendations': recommendations,
            'summary': f"{len(repositories)} Repositories, {len(issues)} Probleme",
            'timestamp': datetime.now().isoformat()
        }
