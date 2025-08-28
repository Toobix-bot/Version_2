"""
Toobix Gamification & UX Revolution
Produktivitäts-Gamification mit Achievements, XP-System und adaptiver UI
"""
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Achievement:
    """Repräsentiert ein Achievement"""
    id: str
    name: str
    description: str
    icon: str
    xp_reward: int
    rarity: str  # common, rare, epic, legendary
    category: str
    unlocked: bool = False
    unlock_date: Optional[datetime] = None
    progress: float = 0.0
    max_progress: float = 100.0

@dataclass
class UserStats:
    """Benutzer-Statistiken"""
    total_xp: int = 0
    level: int = 1
    current_streak: int = 0
    longest_streak: int = 0
    tasks_completed: int = 0
    focus_sessions: int = 0
    total_work_time: float = 0.0
    achievements_unlocked: int = 0
    productivity_score: float = 0.0

@dataclass
class DailyChallenge:
    """Tägliche Herausforderung"""
    id: str
    name: str
    description: str
    target_value: float
    current_progress: float
    xp_reward: int
    bonus_multiplier: float
    expires_at: datetime
    category: str
    difficulty: str

class ProductivityGamification:
    """
    Gamification-System für Produktivitäts-Optimierung
    """
    
    def __init__(self):
        """Initialisiert das Gamification-System"""
        self.user_stats = UserStats()
        self.achievements = {}
        self.daily_challenges = []
        self.activity_log = []
        self.xp_multiplier = 1.0
        
        # Datenverzeichnis
        self.data_dir = Path('toobix_gamification')
        self.data_dir.mkdir(exist_ok=True)
        
        # UI-Konfiguration
        self.ui_config = {
            'theme': 'auto',  # auto, light, dark, cyber
            'animations': True,
            'sound_effects': True,
            'notification_style': 'modern',
            'progress_visualization': 'detailed'
        }
        
        # Initialisierung
        self._load_user_data()
        self._initialize_achievements()
        self._generate_daily_challenges()
        
        logger.info("🎮 Productivity Gamification initialisiert")
    
    def _initialize_achievements(self) -> None:
        """Initialisiert alle verfügbaren Achievements"""
        achievements_data = [
            # Produktivitäts-Achievements
            {
                'id': 'first_task',
                'name': 'Erster Schritt',
                'description': 'Erste Aufgabe erfolgreich abgeschlossen',
                'icon': '🎯',
                'xp_reward': 50,
                'rarity': 'common',
                'category': 'productivity',
                'max_progress': 1
            },
            {
                'id': 'task_master',
                'name': 'Aufgaben-Meister',
                'description': '100 Aufgaben erfolgreich abgeschlossen',
                'icon': '👑',
                'xp_reward': 1000,
                'rarity': 'epic',
                'category': 'productivity',
                'max_progress': 100
            },
            {
                'id': 'focus_warrior',
                'name': 'Fokus-Krieger',
                'description': '25 Pomodoro-Sessions erfolgreich abgeschlossen',
                'icon': '⚔️',
                'xp_reward': 500,
                'rarity': 'rare',
                'category': 'focus',
                'max_progress': 25
            },
            {
                'id': 'streak_master',
                'name': 'Konsistenz-König',
                'description': '30 Tage in Folge produktiv',
                'icon': '🔥',
                'xp_reward': 2000,
                'rarity': 'legendary',
                'category': 'consistency',
                'max_progress': 30
            },
            
            # Zeitmanagement-Achievements
            {
                'id': 'early_bird',
                'name': 'Früher Vogel',
                'description': '10 mal vor 7 Uhr mit der Arbeit begonnen',
                'icon': '🐦',
                'xp_reward': 300,
                'rarity': 'rare',
                'category': 'time_management',
                'max_progress': 10
            },
            {
                'id': 'night_owl',
                'name': 'Nachteule',
                'description': '10 productive Sessions nach 22 Uhr',
                'icon': '🦉',
                'xp_reward': 300,
                'rarity': 'rare',
                'category': 'time_management',
                'max_progress': 10
            },
            
            # Wellness-Achievements
            {
                'id': 'break_master',
                'name': 'Pausen-Profi',
                'description': '50 empfohlene Pausen genommen',
                'icon': '☕',
                'xp_reward': 400,
                'rarity': 'rare',
                'category': 'wellness',
                'max_progress': 50
            },
            {
                'id': 'balance_keeper',
                'name': 'Work-Life-Balance',
                'description': '7 Tage perfekte Work-Life-Balance',
                'icon': '⚖️',
                'xp_reward': 600,
                'rarity': 'epic',
                'category': 'wellness',
                'max_progress': 7
            },
            
            # Skill-Achievements
            {
                'id': 'code_ninja',
                'name': 'Code-Ninja',
                'description': '50 Stunden Programmierung',
                'icon': '🥷',
                'xp_reward': 800,
                'rarity': 'epic',
                'category': 'skills',
                'max_progress': 50
            },
            {
                'id': 'writer_extraordinaire',
                'name': 'Schreib-Virtuose',
                'description': '100.000 Wörter geschrieben',
                'icon': '✍️',
                'xp_reward': 1200,
                'rarity': 'legendary',
                'category': 'skills',
                'max_progress': 100000
            }
        ]
        
        # Achievements laden oder erstellen
        for ach_data in achievements_data:
            achievement = Achievement(**ach_data)
            self.achievements[achievement.id] = achievement
    
    def _generate_daily_challenges(self) -> None:
        """Generiert tägliche Herausforderungen"""
        today = datetime.now().date()
        
        # Prüfen ob bereits Challenges für heute existieren
        existing_challenges = [c for c in self.daily_challenges if c.expires_at.date() == today]
        if existing_challenges:
            return
        
        # Neue Challenges generieren
        challenge_templates = [
            {
                'name': 'Fokus-Marathon',
                'description': 'Arbeite {target} Stunden konzentriert',
                'category': 'focus',
                'target_range': (2, 6),
                'xp_base': 100,
                'difficulty': 'medium'
            },
            {
                'name': 'Task-Bezwinger',
                'description': 'Schließe {target} Aufgaben ab',
                'category': 'productivity',
                'target_range': (5, 15),
                'xp_base': 80,
                'difficulty': 'easy'
            },
            {
                'name': 'Früher Start',
                'description': 'Beginne vor {target} Uhr mit der Arbeit',
                'category': 'time_management',
                'target_range': (7, 9),
                'xp_base': 150,
                'difficulty': 'hard'
            },
            {
                'name': 'Pausen-Meister',
                'description': 'Nimm {target} empfohlene Pausen',
                'category': 'wellness',
                'target_range': (3, 8),
                'xp_base': 120,
                'difficulty': 'medium'
            },
            {
                'name': 'Kontext-Experte',
                'description': 'Arbeite in {target} verschiedenen Kontexten',
                'category': 'variety',
                'target_range': (3, 5),
                'xp_base': 90,
                'difficulty': 'easy'
            }
        ]
        
        # 3 zufällige Challenges für heute
        selected_templates = random.sample(challenge_templates, 3)
        
        for i, template in enumerate(selected_templates):
            target = random.randint(*template['target_range'])
            
            challenge = DailyChallenge(
                id=f"daily_{today.strftime('%Y%m%d')}_{i}",
                name=template['name'],
                description=template['description'].format(target=target),
                target_value=target,
                current_progress=0.0,
                xp_reward=template['xp_base'] + (target * 10),
                bonus_multiplier=1.5 if template['difficulty'] == 'hard' else 1.2 if template['difficulty'] == 'medium' else 1.0,
                expires_at=datetime.combine(today + timedelta(days=1), datetime.min.time()),
                category=template['category'],
                difficulty=template['difficulty']
            )
            
            self.daily_challenges.append(challenge)
        
        logger.info(f"🎯 {len(selected_templates)} Daily Challenges generiert")
    
    def award_xp(self, amount: int, reason: str, category: str = 'general') -> Dict[str, Any]:
        """Vergibt XP und prüft Level-Ups"""
        # XP mit Multiplikator
        final_amount = int(amount * self.xp_multiplier)
        old_level = self.user_stats.level
        
        # XP hinzufügen
        self.user_stats.total_xp += final_amount
        
        # Level berechnen (exponentiell)
        new_level = int((self.user_stats.total_xp / 1000) ** 0.5) + 1
        self.user_stats.level = new_level
        
        # Level-Up Event
        level_up = new_level > old_level
        
        # Activity Log
        self.activity_log.append({
            'timestamp': datetime.now(),
            'type': 'xp_gained',
            'amount': final_amount,
            'reason': reason,
            'category': category,
            'level_up': level_up
        })
        
        # Daten speichern
        self._save_user_data()
        
        result = {
            'xp_gained': final_amount,
            'total_xp': self.user_stats.total_xp,
            'level': self.user_stats.level,
            'level_up': level_up,
            'reason': reason
        }
        
        if level_up:
            logger.info(f"🎉 Level Up! Neues Level: {new_level}")
            result['level_up_message'] = f"Glückwunsch! Du bist jetzt Level {new_level}!"
        
        return result
    
    def complete_task(self, task_name: str, difficulty: str = 'medium', time_spent: float = 0) -> Dict[str, Any]:
        """Registriert abgeschlossene Aufgabe"""
        # XP basierend auf Schwierigkeit
        xp_rewards = {
            'easy': 25,
            'medium': 50,
            'hard': 100,
            'expert': 200
        }
        
        base_xp = xp_rewards.get(difficulty, 50)
        
        # Zeit-Bonus
        time_bonus = min(50, int(time_spent * 5)) if time_spent > 0 else 0
        
        total_xp = base_xp + time_bonus
        
        # Statistiken aktualisieren
        self.user_stats.tasks_completed += 1
        self.user_stats.total_work_time += time_spent
        
        # XP vergeben
        xp_result = self.award_xp(total_xp, f"Aufgabe '{task_name}' abgeschlossen", 'productivity')
        
        # Achievement-Progress aktualisieren
        achievement_updates = []
        
        # Task-bezogene Achievements
        achievement_updates.extend(self._update_achievement_progress('first_task', 1))
        achievement_updates.extend(self._update_achievement_progress('task_master', 1))
        
        # Daily Challenges aktualisieren
        challenge_updates = self._update_daily_challenges('productivity', 1)
        
        return {
            **xp_result,
            'achievements': achievement_updates,
            'challenges': challenge_updates,
            'stats_update': {
                'tasks_completed': self.user_stats.tasks_completed,
                'total_work_time': round(self.user_stats.total_work_time, 1)
            }
        }
    
    def complete_focus_session(self, duration_minutes: float, efficiency_score: float = 80) -> Dict[str, Any]:
        """Registriert abgeschlossene Fokus-Session"""
        # XP basierend auf Dauer und Effizienz
        base_xp = int(duration_minutes * 2)  # 2 XP pro Minute
        efficiency_bonus = int((efficiency_score / 100) * base_xp * 0.5)  # Bis zu 50% Bonus
        
        total_xp = base_xp + efficiency_bonus
        
        # Statistiken aktualisieren
        self.user_stats.focus_sessions += 1
        
        # XP vergeben
        xp_result = self.award_xp(total_xp, f"Fokus-Session ({duration_minutes:.0f}min, {efficiency_score:.0f}% Effizienz)", 'focus')
        
        # Achievement-Progress
        achievement_updates = []
        achievement_updates.extend(self._update_achievement_progress('focus_warrior', 1))
        
        # Spezielle Achievements für lange Sessions
        if duration_minutes >= 90:
            achievement_updates.extend(self._update_achievement_progress('deep_work_master', 1))
        
        # Daily Challenges
        challenge_updates = self._update_daily_challenges('focus', duration_minutes / 60)
        
        return {
            **xp_result,
            'achievements': achievement_updates,
            'challenges': challenge_updates,
            'session_stats': {
                'duration': duration_minutes,
                'efficiency': efficiency_score,
                'total_sessions': self.user_stats.focus_sessions
            }
        }
    
    def _update_achievement_progress(self, achievement_id: str, progress_amount: float) -> List[Dict[str, Any]]:
        """Aktualisiert Achievement-Progress"""
        updates = []
        
        if achievement_id not in self.achievements:
            return updates
        
        achievement = self.achievements[achievement_id]
        
        if achievement.unlocked:
            return updates
        
        # Progress aktualisieren
        old_progress = achievement.progress
        achievement.progress = min(achievement.max_progress, achievement.progress + progress_amount)
        
        # Completion prüfen
        if achievement.progress >= achievement.max_progress and not achievement.unlocked:
            achievement.unlocked = True
            achievement.unlock_date = datetime.now()
            self.user_stats.achievements_unlocked += 1
            
            # XP-Belohnung
            xp_result = self.award_xp(achievement.xp_reward, f"Achievement '{achievement.name}' freigeschaltet!", 'achievement')
            
            updates.append({
                'type': 'achievement_unlocked',
                'achievement': asdict(achievement),
                'xp_reward': achievement.xp_reward
            })
            
            logger.info(f"🏆 Achievement freigeschaltet: {achievement.name}")
        
        elif achievement.progress > old_progress:
            updates.append({
                'type': 'achievement_progress',
                'achievement_id': achievement_id,
                'progress': achievement.progress,
                'max_progress': achievement.max_progress,
                'percentage': (achievement.progress / achievement.max_progress) * 100
            })
        
        return updates
    
    def _update_daily_challenges(self, category: str, progress_amount: float) -> List[Dict[str, Any]]:
        """Aktualisiert Daily Challenge Progress"""
        updates = []
        today = datetime.now().date()
        
        for challenge in self.daily_challenges:
            if (challenge.expires_at.date() == today and 
                challenge.category == category and 
                challenge.current_progress < challenge.target_value):
                
                old_progress = challenge.current_progress
                challenge.current_progress = min(challenge.target_value, challenge.current_progress + progress_amount)
                
                # Completion prüfen
                if challenge.current_progress >= challenge.target_value and old_progress < challenge.target_value:
                    # Challenge abgeschlossen
                    xp_reward = int(challenge.xp_reward * challenge.bonus_multiplier)
                    xp_result = self.award_xp(xp_reward, f"Daily Challenge '{challenge.name}' abgeschlossen!", 'challenge')
                    
                    updates.append({
                        'type': 'challenge_completed',
                        'challenge': asdict(challenge),
                        'xp_reward': xp_reward
                    })
                    
                    logger.info(f"🎯 Daily Challenge abgeschlossen: {challenge.name}")
                
                elif challenge.current_progress > old_progress:
                    updates.append({
                        'type': 'challenge_progress',
                        'challenge_id': challenge.id,
                        'progress': challenge.current_progress,
                        'target': challenge.target_value,
                        'percentage': (challenge.current_progress / challenge.target_value) * 100
                    })
        
        return updates
    
    def get_productivity_dashboard(self) -> Dict[str, Any]:
        """Liefert Gamification-Dashboard"""
        # Current Level Progress
        current_level_xp = (self.user_stats.level - 1) ** 2 * 1000
        next_level_xp = self.user_stats.level ** 2 * 1000
        level_progress = ((self.user_stats.total_xp - current_level_xp) / (next_level_xp - current_level_xp)) * 100
        
        # Recent Achievements
        recent_achievements = [
            ach for ach in self.achievements.values() 
            if ach.unlocked and ach.unlock_date and 
            (datetime.now() - ach.unlock_date).days <= 7
        ]
        
        # Active Daily Challenges
        today = datetime.now().date()
        today_challenges = [
            c for c in self.daily_challenges 
            if c.expires_at.date() == today
        ]
        
        # Productivity Score berechnen
        productivity_score = self._calculate_productivity_score()
        
        return {
            'user_stats': asdict(self.user_stats),
            'level_progress': {
                'current_level': self.user_stats.level,
                'current_xp': self.user_stats.total_xp,
                'next_level_xp': next_level_xp,
                'progress_percentage': min(100, max(0, level_progress))
            },
            'recent_achievements': [asdict(ach) for ach in recent_achievements[-5:]],
            'daily_challenges': [asdict(c) for c in today_challenges],
            'productivity_score': productivity_score,
            'streak_info': {
                'current_streak': self.user_stats.current_streak,
                'longest_streak': self.user_stats.longest_streak,
                'streak_status': self._get_streak_status()
            },
            'top_categories': self._get_top_categories(),
            'motivational_message': self._get_motivational_message()
        }
    
    def _calculate_productivity_score(self) -> float:
        """Berechnet aktuellen Produktivitäts-Score"""
        # Basierend auf verschiedenen Faktoren
        base_score = 50
        
        # XP-basierter Score
        xp_score = min(30, self.user_stats.total_xp / 1000)
        
        # Streak-Score
        streak_score = min(15, self.user_stats.current_streak * 2)
        
        # Achievement-Score
        achievement_score = min(20, self.user_stats.achievements_unlocked * 2)
        
        # Recent Activity Score
        recent_activity = len([
            log for log in self.activity_log 
            if (datetime.now() - log['timestamp']).days <= 1
        ])
        activity_score = min(15, recent_activity * 3)
        
        total_score = base_score + xp_score + streak_score + achievement_score + activity_score
        return min(100, max(0, total_score))
    
    def _get_streak_status(self) -> str:
        """Ermittelt Streak-Status"""
        if self.user_stats.current_streak == 0:
            return "Bereit für einen neuen Start! 🚀"
        elif self.user_stats.current_streak < 3:
            return f"Guter Anfang! {self.user_stats.current_streak} Tage 🌱"
        elif self.user_stats.current_streak < 7:
            return f"Momentum aufgebaut! {self.user_stats.current_streak} Tage 🔥"
        elif self.user_stats.current_streak < 30:
            return f"Fantastische Serie! {self.user_stats.current_streak} Tage ⚡"
        else:
            return f"Legende! {self.user_stats.current_streak} Tage 👑"
    
    def _get_top_categories(self) -> List[Dict[str, Any]]:
        """Ermittelt Top-Aktivitäts-Kategorien"""
        category_stats = defaultdict(lambda: {'xp': 0, 'count': 0})
        
        for log in self.activity_log:
            if log['type'] == 'xp_gained':
                category = log.get('category', 'general')
                category_stats[category]['xp'] += log['amount']
                category_stats[category]['count'] += 1
        
        # Sortiere nach XP
        sorted_categories = sorted(
            category_stats.items(), 
            key=lambda x: x[1]['xp'], 
            reverse=True
        )
        
        return [
            {
                'name': category,
                'xp': stats['xp'],
                'activities': stats['count']
            }
            for category, stats in sorted_categories[:5]
        ]
    
    def _get_motivational_message(self) -> str:
        """Generiert motivierende Nachricht"""
        messages = {
            'morning': [
                "Guten Morgen! Bereit für einen produktiven Tag? ☀️",
                "Ein neuer Tag, neue Möglichkeiten! Los geht's! 🚀",
                "Heute ist der perfekte Tag für Großes! 💪"
            ],
            'afternoon': [
                "Der Tag läuft gut! Weiter so! 🎯",
                "Mittagszeit - perfekt für neue Energie! ⚡",
                "Du schaffst das! Bleib fokussiert! 🔥"
            ],
            'evening': [
                "Was für ein produktiver Tag! Gut gemacht! 🌟",
                "Zeit für eine verdiente Pause! 🏆",
                "Stolz auf deine Leistung heute! 💖"
            ]
        }
        
        hour = datetime.now().hour
        if hour < 12:
            period = 'morning'
        elif hour < 18:
            period = 'afternoon'
        else:
            period = 'evening'
        
        return random.choice(messages[period])
    
    def _load_user_data(self) -> None:
        """Lädt Benutzerdaten"""
        try:
            data_file = self.data_dir / 'user_stats.json'
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_stats = UserStats(**data.get('stats', {}))
                    
                    # Achievements laden
                    achievements_data = data.get('achievements', {})
                    for ach_id, ach_data in achievements_data.items():
                        if ach_id in self.achievements:
                            ach = self.achievements[ach_id]
                            ach.unlocked = ach_data.get('unlocked', False)
                            ach.progress = ach_data.get('progress', 0.0)
                            if ach_data.get('unlock_date'):
                                ach.unlock_date = datetime.fromisoformat(ach_data['unlock_date'])
                    
                    # Activity Log laden
                    activity_data = data.get('activity_log', [])
                    self.activity_log = [
                        {
                            **log,
                            'timestamp': datetime.fromisoformat(log['timestamp'])
                        }
                        for log in activity_data[-100:]  # Nur letzte 100 Einträge
                    ]
                    
        except Exception as e:
            logger.error(f"Fehler beim Laden der Benutzerdaten: {e}")
    
    def _save_user_data(self) -> None:
        """Speichert Benutzerdaten"""
        try:
            data_file = self.data_dir / 'user_stats.json'
            
            # Achievements für Speicherung vorbereiten
            achievements_data = {}
            for ach_id, ach in self.achievements.items():
                achievements_data[ach_id] = {
                    'unlocked': ach.unlocked,
                    'progress': ach.progress,
                    'unlock_date': ach.unlock_date.isoformat() if ach.unlock_date else None
                }
            
            # Activity Log für Speicherung vorbereiten
            activity_data = [
                {
                    **log,
                    'timestamp': log['timestamp'].isoformat()
                }
                for log in self.activity_log[-100:]  # Nur letzte 100 Einträge
            ]
            
            data = {
                'stats': asdict(self.user_stats),
                'achievements': achievements_data,
                'activity_log': activity_data,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Benutzerdaten: {e}")

if __name__ == "__main__":
    # Test des Gamification-Systems
    gamification = ProductivityGamification()
    
    # Test Task Completion
    result = gamification.complete_task("Test-Aufgabe", "medium", 1.5)
    print("Task Completion:", result)
    
    # Test Focus Session
    result = gamification.complete_focus_session(45, 85)
    print("Focus Session:", result)
    
    # Dashboard anzeigen
    dashboard = gamification.get_productivity_dashboard()
    print("Dashboard:", json.dumps(dashboard, indent=2, default=str))
