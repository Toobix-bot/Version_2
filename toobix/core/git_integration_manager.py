"""
Toobix Git Integration Manager
Intelligente Git-Repository-Verwaltung und Automatisierung
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging
import git
from git import Repo, InvalidGitRepositoryError

class GitIntegrationManager:
    """Erweiterte Git-Integration mit intelligenter Repository-Verwaltung"""
    
    def __init__(self, settings=None):
        self.settings = settings
        self.repositories = {}
        self.scan_paths = [
            Path.home() / 'Documents',
            Path.home() / 'Desktop', 
            Path('C:/Code'),
            Path('C:/Projects'),
            Path('C:/Dev'),
            Path('C:/git')
        ]
        self.logger = logging.getLogger('GitIntegrationManager')
        
    def scan_git_repositories(self, custom_paths: List[str] = None) -> Dict:
        """Scannt System nach Git-Repositories"""
        scan_paths = custom_paths if custom_paths else self.scan_paths
        found_repos = {}
        
        self.logger.info("Scanning für Git-Repositories...")
        
        for scan_path in scan_paths:
            if isinstance(scan_path, str):
                scan_path = Path(scan_path)
                
            if not scan_path.exists():
                continue
                
            try:
                # Rekursiv nach .git Ordnern suchen
                for git_dir in scan_path.rglob('.git'):
                    if git_dir.is_dir():
                        repo_path = git_dir.parent
                        try:
                            repo_info = self._analyze_repository(repo_path)
                            if repo_info:
                                found_repos[str(repo_path)] = repo_info
                        except Exception as e:
                            self.logger.warning(f"Fehler bei Repository-Analyse {repo_path}: {e}")
                            
            except PermissionError:
                self.logger.warning(f"Keine Berechtigung für {scan_path}")
            except Exception as e:
                self.logger.error(f"Fehler beim Scannen von {scan_path}: {e}")
        
        self.repositories = found_repos
        self.logger.info(f"{len(found_repos)} Git-Repositories gefunden")
        return found_repos
    
    def _analyze_repository(self, repo_path: Path) -> Optional[Dict]:
        """Analysiert einzelnes Git-Repository"""
        try:
            repo = Repo(str(repo_path))
            
            # Basis-Informationen
            repo_info = {
                'path': str(repo_path),
                'name': repo_path.name,
                'is_bare': repo.bare,
                'is_dirty': repo.is_dirty(),
                'active_branch': repo.active_branch.name if repo.active_branch else None,
                'branches': [branch.name for branch in repo.branches],
                'remotes': [remote.name for remote in repo.remotes],
                'tags': [tag.name for tag in repo.tags],
                'last_commit': None,
                'uncommitted_changes': 0,
                'untracked_files': [],
                'ahead_behind': {'ahead': 0, 'behind': 0},
                'size_mb': 0,
                'file_count': 0,
                'language_stats': {},
                'health_score': 100
            }
            
            # Letzter Commit
            try:
                last_commit = repo.head.commit
                repo_info['last_commit'] = {
                    'hash': last_commit.hexsha[:8],
                    'message': last_commit.message.strip(),
                    'author': str(last_commit.author),
                    'date': last_commit.committed_datetime.isoformat(),
                    'days_ago': (datetime.now() - last_commit.committed_datetime.replace(tzinfo=None)).days
                }
            except Exception:
                pass
            
            # Uncommitted Changes
            try:
                repo_info['uncommitted_changes'] = len(repo.index.diff(None)) + len(repo.index.diff("HEAD"))
                repo_info['untracked_files'] = repo.untracked_files
            except Exception:
                pass
            
            # Remote-Status (Ahead/Behind)
            try:
                if repo.remotes:
                    origin = repo.remotes.origin
                    repo_info['ahead_behind'] = self._get_ahead_behind_count(repo, origin)
            except Exception:
                pass
            
            # Repository-Größe
            try:
                total_size = 0
                file_count = 0
                for root, dirs, files in os.walk(repo_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            total_size += os.path.getsize(file_path)
                            file_count += 1
                        except:
                            pass
                repo_info['size_mb'] = round(total_size / (1024 * 1024), 2)
                repo_info['file_count'] = file_count
            except Exception:
                pass
            
            # Programmiersprachen-Statistiken
            try:
                repo_info['language_stats'] = self._analyze_languages(repo_path)
            except Exception:
                pass
            
            # Repository-Gesundheit bewerten
            repo_info['health_score'] = self._calculate_repo_health(repo_info)
            
            return repo_info
            
        except InvalidGitRepositoryError:
            return None
        except Exception as e:
            self.logger.error(f"Fehler bei Repository-Analyse {repo_path}: {e}")
            return None
    
    def _get_ahead_behind_count(self, repo: Repo, remote) -> Dict:
        """Ermittelt Ahead/Behind-Count zum Remote"""
        try:
            # Fetch latest remote info
            remote.fetch()
            
            local_branch = repo.active_branch
            remote_branch = f"{remote.name}/{local_branch.name}"
            
            # Count commits ahead/behind
            ahead_commits = list(repo.iter_commits(f'{remote_branch}..{local_branch.name}'))
            behind_commits = list(repo.iter_commits(f'{local_branch.name}..{remote_branch}'))
            
            return {
                'ahead': len(ahead_commits),
                'behind': len(behind_commits)
            }
        except Exception:
            return {'ahead': 0, 'behind': 0}
    
    def _analyze_languages(self, repo_path: Path) -> Dict:
        """Analysiert Programmiersprachen im Repository"""
        language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript', 
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.php': 'PHP',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.scala': 'Scala',
            '.html': 'HTML',
            '.css': 'CSS',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.ps1': 'PowerShell',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.json': 'JSON',
            '.xml': 'XML',
            '.md': 'Markdown'
        }
        
        language_stats = {}
        
        try:
            for file_path in repo_path.rglob('*'):
                if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts[len(repo_path.parts):]):
                    extension = file_path.suffix.lower()
                    if extension in language_extensions:
                        language = language_extensions[extension]
                        if language not in language_stats:
                            language_stats[language] = {'files': 0, 'lines': 0}
                        
                        language_stats[language]['files'] += 1
                        
                        # Zeilen zählen
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                lines = sum(1 for line in f if line.strip())
                                language_stats[language]['lines'] += lines
                        except:
                            pass
        except Exception:
            pass
        
        return language_stats
    
    def _calculate_repo_health(self, repo_info: Dict) -> int:
        """Berechnet Repository-Gesundheitsscore"""
        score = 100
        
        try:
            # Uncommitted Changes (Abzug)
            if repo_info.get('uncommitted_changes', 0) > 10:
                score -= 20
            elif repo_info.get('uncommitted_changes', 0) > 5:
                score -= 10
            
            # Untracked Files (Abzug)
            if len(repo_info.get('untracked_files', [])) > 10:
                score -= 15
            elif len(repo_info.get('untracked_files', [])) > 5:
                score -= 5
            
            # Remote-Sync (Abzug wenn out of sync)
            ahead_behind = repo_info.get('ahead_behind', {})
            if ahead_behind.get('behind', 0) > 5:
                score -= 15
            elif ahead_behind.get('behind', 0) > 0:
                score -= 5
            
            # Alter des letzten Commits (Abzug)
            last_commit = repo_info.get('last_commit')
            if last_commit:
                days_ago = last_commit.get('days_ago', 0)
                if days_ago > 90:
                    score -= 20
                elif days_ago > 30:
                    score -= 10
            
            # Hat Remote (Bonus)
            if repo_info.get('remotes'):
                score += 10
            
            # Mehrere Branches (Bonus)
            if len(repo_info.get('branches', [])) > 1:
                score += 5
            
            return max(0, min(100, score))
            
        except Exception:
            return 50
    
    def get_repository_dashboard(self) -> Dict:
        """Erstellt Repository-Dashboard"""
        if not self.repositories:
            self.scan_git_repositories()
        
        total_repos = len(self.repositories)
        healthy_repos = sum(1 for repo in self.repositories.values() if repo.get('health_score', 0) >= 80)
        repos_with_changes = sum(1 for repo in self.repositories.values() if repo.get('uncommitted_changes', 0) > 0)
        repos_behind = sum(1 for repo in self.repositories.values() if repo.get('ahead_behind', {}).get('behind', 0) > 0)
        
        # Top-Sprachen
        all_languages = {}
        for repo in self.repositories.values():
            for lang, stats in repo.get('language_stats', {}).items():
                if lang not in all_languages:
                    all_languages[lang] = {'files': 0, 'lines': 0, 'repos': 0}
                all_languages[lang]['files'] += stats.get('files', 0)
                all_languages[lang]['lines'] += stats.get('lines', 0)
                all_languages[lang]['repos'] += 1
        
        # Sortierung nach Zeilen
        top_languages = sorted(all_languages.items(), key=lambda x: x[1]['lines'], reverse=True)[:5]
        
        return {
            'summary': {
                'total_repositories': total_repos,
                'healthy_repositories': healthy_repos,
                'repositories_with_changes': repos_with_changes,
                'repositories_behind': repos_behind,
                'health_percentage': round((healthy_repos / total_repos * 100) if total_repos > 0 else 0, 1)
            },
            'top_languages': [
                {
                    'language': lang,
                    'files': stats['files'],
                    'lines': stats['lines'],
                    'repositories': stats['repos']
                }
                for lang, stats in top_languages
            ],
            'problem_repositories': [
                {
                    'name': repo['name'],
                    'path': repo['path'],
                    'health_score': repo['health_score'],
                    'issues': self._identify_repo_issues(repo)
                }
                for repo in self.repositories.values()
                if repo.get('health_score', 100) < 80
            ]
        }
    
    def _identify_repo_issues(self, repo_info: Dict) -> List[str]:
        """Identifiziert spezifische Repository-Probleme"""
        issues = []
        
        if repo_info.get('uncommitted_changes', 0) > 0:
            issues.append(f"{repo_info['uncommitted_changes']} uncommitted changes")
        
        if repo_info.get('untracked_files'):
            issues.append(f"{len(repo_info['untracked_files'])} untracked files")
        
        ahead_behind = repo_info.get('ahead_behind', {})
        if ahead_behind.get('behind', 0) > 0:
            issues.append(f"{ahead_behind['behind']} commits behind remote")
        
        if ahead_behind.get('ahead', 0) > 0:
            issues.append(f"{ahead_behind['ahead']} commits ahead (unpushed)")
        
        last_commit = repo_info.get('last_commit')
        if last_commit and last_commit.get('days_ago', 0) > 30:
            issues.append(f"Last commit {last_commit['days_ago']} days ago")
        
        return issues
    
    def bulk_git_operations(self, operation: str, repo_paths: List[str] = None) -> Dict:
        """Führt Git-Operationen auf mehreren Repositories aus"""
        if repo_paths is None:
            repo_paths = list(self.repositories.keys())
        
        results = {
            'operation': operation,
            'total': len(repo_paths),
            'successful': [],
            'failed': [],
            'skipped': []
        }
        
        for repo_path in repo_paths:
            try:
                repo = Repo(repo_path)
                result = {'path': repo_path, 'name': Path(repo_path).name}
                
                if operation == 'status':
                    result['status'] = self._get_repo_status(repo)
                    results['successful'].append(result)
                    
                elif operation == 'pull':
                    if repo.remotes:
                        repo.remotes.origin.pull()
                        result['message'] = 'Pulled successfully'
                        results['successful'].append(result)
                    else:
                        result['error'] = 'No remotes configured'
                        results['skipped'].append(result)
                        
                elif operation == 'push':
                    if repo.remotes and not repo.is_dirty():
                        repo.remotes.origin.push()
                        result['message'] = 'Pushed successfully'
                        results['successful'].append(result)
                    else:
                        result['error'] = 'No remotes or uncommitted changes'
                        results['skipped'].append(result)
                        
                elif operation == 'commit':
                    if repo.is_dirty():
                        repo.git.add(A=True)
                        commit = repo.index.commit(f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                        result['message'] = f'Committed: {commit.hexsha[:8]}'
                        results['successful'].append(result)
                    else:
                        result['error'] = 'No changes to commit'
                        results['skipped'].append(result)
                        
                else:
                    result['error'] = f'Unknown operation: {operation}'
                    results['failed'].append(result)
                    
            except Exception as e:
                results['failed'].append({
                    'path': repo_path,
                    'name': Path(repo_path).name,
                    'error': str(e)
                })
        
        return results
    
    def _get_repo_status(self, repo: Repo) -> Dict:
        """Ermittelt detaillierten Repository-Status"""
        try:
            return {
                'branch': repo.active_branch.name if repo.active_branch else None,
                'is_dirty': repo.is_dirty(),
                'uncommitted_files': len(repo.index.diff(None)) + len(repo.index.diff("HEAD")),
                'untracked_files': len(repo.untracked_files),
                'last_commit': repo.head.commit.hexsha[:8] if repo.head.commit else None,
                'remotes': [remote.name for remote in repo.remotes]
            }
        except Exception as e:
            return {'error': str(e)}
    
    def auto_commit_and_push(self, repo_path: str, commit_message: str = None) -> Dict:
        """Automatisches Commit und Push"""
        try:
            repo = Repo(repo_path)
            
            if not repo.is_dirty() and not repo.untracked_files:
                return {'success': False, 'message': 'No changes to commit'}
            
            # Add all changes
            repo.git.add(A=True)
            
            # Commit
            if not commit_message:
                commit_message = f"Auto-commit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            commit = repo.index.commit(commit_message)
            
            # Push if remote exists
            push_result = None
            if repo.remotes:
                try:
                    push_info = repo.remotes.origin.push()
                    push_result = 'Pushed successfully'
                except Exception as e:
                    push_result = f'Push failed: {str(e)}'
            
            return {
                'success': True,
                'commit_hash': commit.hexsha[:8],
                'commit_message': commit_message,
                'push_result': push_result,
                'files_changed': len(repo.index.diff("HEAD~1")) if commit else 0
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def cleanup_repositories(self) -> Dict:
        """Cleanup-Operationen für alle Repositories"""
        results = {
            'total': len(self.repositories),
            'cleaned': [],
            'errors': []
        }
        
        for repo_path, repo_info in self.repositories.items():
            try:
                repo = Repo(repo_path)
                cleanup_actions = []
                
                # Git GC (Garbage Collection)
                repo.git.gc()
                cleanup_actions.append('git gc')
                
                # Prune remote branches
                if repo.remotes:
                    repo.remotes.origin.prune()
                    cleanup_actions.append('pruned remotes')
                
                results['cleaned'].append({
                    'path': repo_path,
                    'name': repo_info['name'],
                    'actions': cleanup_actions
                })
                
            except Exception as e:
                results['errors'].append({
                    'path': repo_path,
                    'error': str(e)
                })
        
        return results
