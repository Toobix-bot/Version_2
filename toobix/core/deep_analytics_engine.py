"""
Toobix Deep Analytics Engine
Machine Learning für Produktivitäts-Patterns und Optimierung
"""
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging
import math
import statistics

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProductivityPattern:
    """Produktivitäts-Muster"""
    pattern_id: str
    name: str
    description: str
    confidence: float
    triggers: List[str]
    optimal_conditions: Dict[str, Any]
    average_performance: float
    frequency: str

@dataclass
class PredictiveInsight:
    """Vorhersage-Insight"""
    insight_id: str
    type: str  # performance, energy, distraction, optimal_time
    prediction: str
    confidence: float
    time_horizon: int  # Stunden
    actionable_advice: List[str]
    expected_impact: float

@dataclass
class BehavioralMetric:
    """Verhaltens-Metrik"""
    timestamp: datetime
    context: str
    focus_score: float
    efficiency: float
    energy_level: float
    interruptions: int
    task_switches: int
    session_duration: float
    time_of_day: int
    day_of_week: int

class DeepAnalyticsEngine:
    """
    Deep Analytics für Produktivitäts-Optimierung mit ML
    """
    
    def __init__(self):
        """Initialisiert Analytics Engine"""
        self.behavioral_data = deque(maxlen=1000)  # Letzte 1000 Datenpunkte
        self.productivity_patterns = {}
        self.predictive_models = {}
        self.insights_history = []
        
        # Analytics-Konfiguration
        self.analysis_config = {
            'min_data_points': 10,
            'pattern_confidence_threshold': 0.7,
            'prediction_horizon_hours': 24,
            'learning_rate': 0.1
        }
        
        # Datenverzeichnis
        self.data_dir = Path('toobix_analytics')
        self.data_dir.mkdir(exist_ok=True)
        
        # Initialisierung
        self._load_historical_data()
        
        logger.info("🔬 Deep Analytics Engine initialisiert")
    
    def add_behavioral_data(self, context: str, focus_score: float, efficiency: float, 
                          energy_level: float, interruptions: int = 0, 
                          task_switches: int = 0, session_duration: float = 0) -> None:
        """Fügt neue Verhaltens-Daten hinzu"""
        now = datetime.now()
        
        metric = BehavioralMetric(
            timestamp=now,
            context=context,
            focus_score=focus_score,
            efficiency=efficiency,
            energy_level=energy_level,
            interruptions=interruptions,
            task_switches=task_switches,
            session_duration=session_duration,
            time_of_day=now.hour,
            day_of_week=now.weekday()
        )
        
        self.behavioral_data.append(metric)
        
        # Periodische Analyse
        if len(self.behavioral_data) % 10 == 0:
            self._analyze_patterns()
        
        # Daten speichern
        self._save_data()
    
    def _analyze_patterns(self) -> None:
        """Analysiert Produktivitäts-Muster"""
        if len(self.behavioral_data) < self.analysis_config['min_data_points']:
            return
        
        try:
            # Verschiedene Pattern-Analysen
            self._analyze_time_patterns()
            self._analyze_context_patterns()
            self._analyze_energy_patterns()
            self._analyze_efficiency_patterns()
            
            logger.info("🔍 Pattern-Analyse abgeschlossen")
            
        except Exception as e:
            logger.error(f"Pattern-Analyse Fehler: {e}")
    
    def _analyze_time_patterns(self) -> None:
        """Analysiert zeitbasierte Muster"""
        # Daten nach Stunden gruppieren
        hourly_performance = defaultdict(list)
        
        for metric in self.behavioral_data:
            hour = metric.time_of_day
            performance = (metric.focus_score + metric.efficiency + metric.energy_level) / 3
            hourly_performance[hour].append(performance)
        
        # Durchschnittliche Performance pro Stunde
        hourly_averages = {}
        for hour, performances in hourly_performance.items():
            if len(performances) >= 3:  # Mindestens 3 Datenpunkte
                hourly_averages[hour] = statistics.mean(performances)
        
        if hourly_averages:
            # Beste Stunden identifizieren
            best_hours = sorted(hourly_averages.items(), key=lambda x: x[1], reverse=True)[:3]
            worst_hours = sorted(hourly_averages.items(), key=lambda x: x[1])[:2]
            
            # Pattern erstellen
            pattern = ProductivityPattern(
                pattern_id="time_performance",
                name="Zeitbasierte Leistung",
                description=f"Beste Performance: {[f'{h}:00' for h, _ in best_hours]}",
                confidence=0.8,
                triggers=[f"hour_{h}" for h, _ in best_hours],
                optimal_conditions={
                    'best_hours': [h for h, _ in best_hours],
                    'worst_hours': [h for h, _ in worst_hours],
                    'performance_variance': statistics.stdev(hourly_averages.values()) if len(hourly_averages) > 1 else 0
                },
                average_performance=statistics.mean(hourly_averages.values()),
                frequency="daily"
            )
            
            self.productivity_patterns["time_performance"] = pattern
    
    def _analyze_context_patterns(self) -> None:
        """Analysiert kontext-basierte Muster"""
        context_performance = defaultdict(list)
        
        for metric in self.behavioral_data:
            performance = (metric.focus_score + metric.efficiency) / 2
            context_performance[metric.context].append(performance)
        
        # Durchschnittliche Performance pro Kontext
        context_averages = {}
        for context, performances in context_performance.items():
            if len(performances) >= 3:
                context_averages[context] = {
                    'mean': statistics.mean(performances),
                    'std': statistics.stdev(performances) if len(performances) > 1 else 0,
                    'count': len(performances)
                }
        
        if context_averages:
            # Besten Kontext identifizieren
            best_context = max(context_averages.items(), key=lambda x: x[1]['mean'])
            
            pattern = ProductivityPattern(
                pattern_id="context_performance",
                name="Kontext-Optimierung",
                description=f"Beste Performance in: {best_context[0]}",
                confidence=min(0.9, best_context[1]['count'] / 20),  # Höhere Confidence mit mehr Daten
                triggers=[f"context_{best_context[0]}"],
                optimal_conditions={
                    'best_context': best_context[0],
                    'performance_score': best_context[1]['mean'],
                    'consistency': 1 / (1 + best_context[1]['std'])  # Niedrige Standardabweichung = hohe Konsistenz
                },
                average_performance=best_context[1]['mean'],
                frequency="contextual"
            )
            
            self.productivity_patterns["context_performance"] = pattern
    
    def _analyze_energy_patterns(self) -> None:
        """Analysiert Energy-Level Muster"""
        # Energy vs. Performance Korrelation
        energy_levels = [m.energy_level for m in self.behavioral_data]
        performance_scores = [(m.focus_score + m.efficiency) / 2 for m in self.behavioral_data]
        
        if len(energy_levels) >= 10:
            correlation = self._calculate_correlation(energy_levels, performance_scores)
            
            # Energy-Schwellen identifizieren
            high_energy_threshold = statistics.quantile(energy_levels, 0.75)
            low_energy_threshold = statistics.quantile(energy_levels, 0.25)
            
            # Performance bei verschiedenen Energy-Levels
            high_energy_performance = statistics.mean([
                perf for energy, perf in zip(energy_levels, performance_scores)
                if energy >= high_energy_threshold
            ])
            
            low_energy_performance = statistics.mean([
                perf for energy, perf in zip(energy_levels, performance_scores)
                if energy <= low_energy_threshold
            ])
            
            pattern = ProductivityPattern(
                pattern_id="energy_performance",
                name="Energy-Performance Korrelation",
                description=f"Korrelation: {correlation:.2f}",
                confidence=abs(correlation),
                triggers=["high_energy", "optimal_energy"],
                optimal_conditions={
                    'high_energy_threshold': high_energy_threshold,
                    'low_energy_threshold': low_energy_threshold,
                    'correlation': correlation,
                    'high_energy_performance': high_energy_performance,
                    'low_energy_performance': low_energy_performance
                },
                average_performance=statistics.mean(performance_scores),
                frequency="continuous"
            )
            
            self.productivity_patterns["energy_performance"] = pattern
    
    def _analyze_efficiency_patterns(self) -> None:
        """Analysiert Effizienz-Muster"""
        # Session-Länge vs. Effizienz
        session_durations = [m.session_duration for m in self.behavioral_data if m.session_duration > 0]
        session_efficiencies = [m.efficiency for m in self.behavioral_data if m.session_duration > 0]
        
        if len(session_durations) >= 5:
            # Optimale Session-Länge finden
            duration_efficiency_pairs = list(zip(session_durations, session_efficiencies))
            
            # In Buckets gruppieren (15min Intervalle)
            bucket_efficiency = defaultdict(list)
            for duration, efficiency in duration_efficiency_pairs:
                bucket = int(duration // 15) * 15  # 0, 15, 30, 45, etc.
                bucket_efficiency[bucket].append(efficiency)
            
            # Durchschnittliche Effizienz pro Bucket
            bucket_averages = {}
            for bucket, efficiencies in bucket_efficiency.items():
                if len(efficiencies) >= 2:
                    bucket_averages[bucket] = statistics.mean(efficiencies)
            
            if bucket_averages:
                optimal_duration = max(bucket_averages.items(), key=lambda x: x[1])
                
                pattern = ProductivityPattern(
                    pattern_id="session_efficiency",
                    name="Optimale Session-Länge",
                    description=f"Beste Effizienz bei {optimal_duration[0]}min Sessions",
                    confidence=min(0.8, len(bucket_averages) / 5),
                    triggers=[f"session_duration_{optimal_duration[0]}"],
                    optimal_conditions={
                        'optimal_duration_minutes': optimal_duration[0],
                        'optimal_efficiency': optimal_duration[1],
                        'duration_buckets': dict(bucket_averages)
                    },
                    average_performance=statistics.mean(session_efficiencies),
                    frequency="session_based"
                )
                
                self.productivity_patterns["session_efficiency"] = pattern
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Berechnet Pearson-Korrelation"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        
        sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
        sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
        
        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        
        return numerator / denominator if denominator != 0 else 0.0
    
    def generate_predictions(self) -> List[PredictiveInsight]:
        """Generiert Vorhersagen basierend auf Mustern"""
        predictions = []
        
        if len(self.behavioral_data) < 5:
            return predictions
        
        try:
            # Performance-Vorhersage
            predictions.extend(self._predict_performance())
            
            # Energy-Level Vorhersage
            predictions.extend(self._predict_energy_patterns())
            
            # Optimale Arbeitszeit-Vorhersage
            predictions.extend(self._predict_optimal_work_times())
            
            # Distraktions-Vorhersage
            predictions.extend(self._predict_distraction_risks())
            
            self.insights_history.extend(predictions)
            
        except Exception as e:
            logger.error(f"Vorhersage-Fehler: {e}")
        
        return predictions
    
    def _predict_performance(self) -> List[PredictiveInsight]:
        """Vorhersage der Performance"""
        predictions = []
        
        if "time_performance" in self.productivity_patterns:
            pattern = self.productivity_patterns["time_performance"]
            best_hours = pattern.optimal_conditions['best_hours']
            current_hour = datetime.now().hour
            
            # Nächste beste Stunde finden
            next_optimal_hours = [h for h in best_hours if h > current_hour]
            if not next_optimal_hours:
                next_optimal_hours = best_hours  # Nächster Tag
            
            next_hour = min(next_optimal_hours)
            hours_until = next_hour - current_hour if next_hour > current_hour else (24 - current_hour + next_hour)
            
            prediction = PredictiveInsight(
                insight_id=f"performance_prediction_{datetime.now().strftime('%Y%m%d_%H%M')}",
                type="performance",
                prediction=f"Beste Performance erwartet um {next_hour}:00 Uhr",
                confidence=pattern.confidence,
                time_horizon=hours_until,
                actionable_advice=[
                    f"Plane komplexe Aufgaben für {next_hour}:00 Uhr",
                    "Nutze diese Zeit für wichtige Projekte",
                    "Vermeide Meetings in dieser Zeit"
                ],
                expected_impact=pattern.average_performance
            )
            
            predictions.append(prediction)
        
        return predictions
    
    def _predict_energy_patterns(self) -> List[PredictiveInsight]:
        """Vorhersage von Energy-Patterns"""
        predictions = []
        
        if "energy_performance" in self.productivity_patterns:
            pattern = self.productivity_patterns["energy_performance"]
            correlation = pattern.optimal_conditions['correlation']
            
            # Aktuelle Energy-Trend analysieren
            recent_energy = [m.energy_level for m in list(self.behavioral_data)[-5:]]
            if len(recent_energy) >= 3:
                energy_trend = statistics.mean(recent_energy[-3:]) - statistics.mean(recent_energy[:2])
                
                if energy_trend > 5:
                    prediction_text = "Energy-Level steigt - optimale Zeit für anspruchsvolle Aufgaben"
                    advice = [
                        "Nutze den Energy-Anstieg für komplexe Projekte",
                        "Plane wichtige Entscheidungen jetzt",
                        "Vermeide Routine-Aufgaben"
                    ]
                elif energy_trend < -5:
                    prediction_text = "Energy-Level sinkt - Zeit für leichtere Aufgaben oder Pause"
                    advice = [
                        "Wechsle zu einfacheren Aufgaben",
                        "Plane eine Pause ein",
                        "Vermeide neue komplexe Projekte"
                    ]
                else:
                    prediction_text = "Stabiles Energy-Level - normale Produktivität erwartet"
                    advice = [
                        "Normale Arbeitsplanung beibehalten",
                        "Achte auf Energie-Signale",
                        "Bereite dich auf Energy-Schwankungen vor"
                    ]
                
                prediction = PredictiveInsight(
                    insight_id=f"energy_prediction_{datetime.now().strftime('%Y%m%d_%H%M')}",
                    type="energy",
                    prediction=prediction_text,
                    confidence=min(0.8, abs(correlation)),
                    time_horizon=2,
                    actionable_advice=advice,
                    expected_impact=abs(energy_trend) / 10
                )
                
                predictions.append(prediction)
        
        return predictions
    
    def _predict_optimal_work_times(self) -> List[PredictiveInsight]:
        """Vorhersage optimaler Arbeitszeiten"""
        predictions = []
        
        # Basierend auf historischen Daten
        hourly_performance = defaultdict(list)
        for metric in self.behavioral_data:
            performance = (metric.focus_score + metric.efficiency) / 2
            hourly_performance[metric.time_of_day].append(performance)
        
        if len(hourly_performance) >= 3:
            # Heute noch verbleibende Stunden analysieren
            current_hour = datetime.now().hour
            remaining_hours = list(range(current_hour + 1, 24))
            
            # Performance-Vorhersage für verbleibende Stunden
            hour_predictions = []
            for hour in remaining_hours:
                if hour in hourly_performance and len(hourly_performance[hour]) >= 2:
                    avg_performance = statistics.mean(hourly_performance[hour])
                    hour_predictions.append((hour, avg_performance))
            
            if hour_predictions:
                # Beste verbleibende Stunde
                best_hour = max(hour_predictions, key=lambda x: x[1])
                
                prediction = PredictiveInsight(
                    insight_id=f"optimal_time_{datetime.now().strftime('%Y%m%d_%H%M')}",
                    type="optimal_time",
                    prediction=f"Heute um {best_hour[0]}:00 Uhr beste Produktivität erwartet",
                    confidence=0.7,
                    time_horizon=best_hour[0] - current_hour,
                    actionable_advice=[
                        f"Reserviere {best_hour[0]}:00 Uhr für wichtige Aufgaben",
                        "Plane weniger wichtige Tasks für andere Zeiten",
                        "Nutze diese Vorhersage für deine Tagesplanung"
                    ],
                    expected_impact=best_hour[1]
                )
                
                predictions.append(prediction)
        
        return predictions
    
    def _predict_distraction_risks(self) -> List[PredictiveInsight]:
        """Vorhersage von Distraktions-Risiken"""
        predictions = []
        
        # Analyse der Interruption-Patterns
        interruption_data = [(m.timestamp, m.interruptions) for m in self.behavioral_data if m.interruptions > 0]
        
        if len(interruption_data) >= 5:
            # Zeitliche Muster in Interruptions
            hourly_interruptions = defaultdict(list)
            for timestamp, interruptions in interruption_data:
                hourly_interruptions[timestamp.hour].append(interruptions)
            
            # Durchschnittliche Interruptions pro Stunde
            risky_hours = []
            for hour, interruptions in hourly_interruptions.items():
                if len(interruptions) >= 2:
                    avg_interruptions = statistics.mean(interruptions)
                    if avg_interruptions > 2:  # Threshold für "risky"
                        risky_hours.append((hour, avg_interruptions))
            
            if risky_hours:
                current_hour = datetime.now().hour
                upcoming_risky_hours = [h for h, _ in risky_hours if h > current_hour]
                
                if upcoming_risky_hours:
                    next_risky_hour = min(upcoming_risky_hours)
                    
                    prediction = PredictiveInsight(
                        insight_id=f"distraction_risk_{datetime.now().strftime('%Y%m%d_%H%M')}",
                        type="distraction",
                        prediction=f"Erhöhtes Distraktions-Risiko um {next_risky_hour}:00 Uhr",
                        confidence=0.6,
                        time_horizon=next_risky_hour - current_hour,
                        actionable_advice=[
                            "Plane wichtige Deep-Work vor dieser Zeit",
                            "Bereite Distraktions-Blocker vor",
                            "Verwende Focus-Modi in dieser Zeit",
                            "Plane administrative Aufgaben für diese Zeit"
                        ],
                        expected_impact=-0.3  # Negative Impact
                    )
                    
                    predictions.append(prediction)
        
        return predictions
    
    def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Liefert umfassendes Analytics-Dashboard"""
        try:
            dashboard = {
                'overview': {
                    'data_points': len(self.behavioral_data),
                    'patterns_identified': len(self.productivity_patterns),
                    'analysis_confidence': self._calculate_overall_confidence(),
                    'last_analysis': datetime.now().isoformat()
                },
                'productivity_patterns': {
                    pattern_id: asdict(pattern) 
                    for pattern_id, pattern in self.productivity_patterns.items()
                },
                'recent_insights': [
                    asdict(insight) for insight in self.insights_history[-5:]
                ],
                'performance_trends': self._analyze_performance_trends(),
                'optimization_opportunities': self._identify_optimization_opportunities(),
                'recommendations': self._generate_smart_recommendations()
            }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Dashboard-Fehler: {e}")
            return {'error': str(e)}
    
    def _calculate_overall_confidence(self) -> float:
        """Berechnet Gesamt-Confidence der Analyse"""
        if not self.productivity_patterns:
            return 0.0
        
        confidences = [pattern.confidence for pattern in self.productivity_patterns.values()]
        data_factor = min(1.0, len(self.behavioral_data) / 100)  # Mehr Daten = höhere Confidence
        
        return statistics.mean(confidences) * data_factor
    
    def _analyze_performance_trends(self) -> Dict[str, Any]:
        """Analysiert Performance-Trends"""
        if len(self.behavioral_data) < 5:
            return {}
        
        # Letzte 7 Tage vs. vorherige 7 Tage
        now = datetime.now()
        last_week = [m for m in self.behavioral_data if (now - m.timestamp).days <= 7]
        prev_week = [m for m in self.behavioral_data if 7 < (now - m.timestamp).days <= 14]
        
        trends = {}
        
        if last_week and prev_week:
            # Performance-Vergleich
            last_week_perf = statistics.mean([(m.focus_score + m.efficiency) / 2 for m in last_week])
            prev_week_perf = statistics.mean([(m.focus_score + m.efficiency) / 2 for m in prev_week])
            
            trends['performance_change'] = ((last_week_perf - prev_week_perf) / prev_week_perf) * 100
            trends['trend_direction'] = 'improving' if trends['performance_change'] > 0 else 'declining'
            
            # Energy-Trend
            last_week_energy = statistics.mean([m.energy_level for m in last_week])
            prev_week_energy = statistics.mean([m.energy_level for m in prev_week])
            
            trends['energy_change'] = ((last_week_energy - prev_week_energy) / prev_week_energy) * 100
        
        return trends
    
    def _identify_optimization_opportunities(self) -> List[Dict[str, Any]]:
        """Identifiziert Optimierungs-Möglichkeiten"""
        opportunities = []
        
        if len(self.behavioral_data) < 10:
            return opportunities
        
        # Niedrige Effizienz-Zeiten identifizieren
        low_efficiency_sessions = [m for m in self.behavioral_data if m.efficiency < 60]
        if len(low_efficiency_sessions) > len(self.behavioral_data) * 0.3:  # Mehr als 30% niedrige Effizienz
            common_contexts = defaultdict(int)
            for session in low_efficiency_sessions:
                common_contexts[session.context] += 1
            
            if common_contexts:
                worst_context = max(common_contexts.items(), key=lambda x: x[1])
                opportunities.append({
                    'type': 'context_optimization',
                    'title': 'Kontext-Optimierung',
                    'description': f'Niedrige Effizienz in "{worst_context[0]}" - {worst_context[1]} mal',
                    'impact': 'medium',
                    'effort': 'low'
                })
        
        # Hohe Interruption-Zeiten
        high_interruption_sessions = [m for m in self.behavioral_data if m.interruptions > 3]
        if len(high_interruption_sessions) > 5:
            opportunities.append({
                'type': 'distraction_management',
                'title': 'Distraktions-Management',
                'description': f'{len(high_interruption_sessions)} Sessions mit hohen Unterbrechungen',
                'impact': 'high',
                'effort': 'medium'
            })
        
        # Suboptimale Session-Längen
        if "session_efficiency" in self.productivity_patterns:
            pattern = self.productivity_patterns["session_efficiency"]
            optimal_duration = pattern.optimal_conditions['optimal_duration_minutes']
            
            suboptimal_sessions = [
                m for m in self.behavioral_data 
                if m.session_duration > 0 and abs(m.session_duration - optimal_duration) > 15
            ]
            
            if len(suboptimal_sessions) > len(self.behavioral_data) * 0.4:
                opportunities.append({
                    'type': 'session_timing',
                    'title': 'Session-Timing Optimierung',
                    'description': f'Optimale Session-Länge: {optimal_duration}min',
                    'impact': 'medium',
                    'effort': 'low'
                })
        
        return opportunities
    
    def _generate_smart_recommendations(self) -> List[str]:
        """Generiert intelligente Empfehlungen"""
        recommendations = []
        
        if len(self.behavioral_data) < 5:
            recommendations.append("🔍 Sammle mehr Daten für präzisere Empfehlungen")
            return recommendations
        
        # Basierend auf Patterns
        if "time_performance" in self.productivity_patterns:
            pattern = self.productivity_patterns["time_performance"]
            best_hours = pattern.optimal_conditions['best_hours']
            recommendations.append(f"⏰ Plane wichtige Aufgaben für {best_hours[0]}:00-{best_hours[0]+2}:00 Uhr")
        
        if "energy_performance" in self.productivity_patterns:
            pattern = self.productivity_patterns["energy_performance"]
            correlation = pattern.optimal_conditions['correlation']
            if correlation > 0.5:
                recommendations.append("🔋 Starke Energy-Performance Korrelation - achte auf dein Energy-Level!")
        
        # Aktuelle Vorhersagen berücksichtigen
        recent_predictions = self.generate_predictions()
        for prediction in recent_predictions:
            if prediction.confidence > 0.7:
                recommendations.append(f"🔮 {prediction.prediction}")
        
        return recommendations[:5]  # Top 5 Empfehlungen
    
    def _load_historical_data(self) -> None:
        """Lädt historische Analytics-Daten"""
        try:
            data_file = self.data_dir / 'analytics_data.json'
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Behavioral Data laden
                    behavioral_data = data.get('behavioral_data', [])
                    for item in behavioral_data[-100:]:  # Letzte 100 Einträge
                        try:
                            metric = BehavioralMetric(
                                timestamp=datetime.fromisoformat(item['timestamp']),
                                context=item['context'],
                                focus_score=item['focus_score'],
                                efficiency=item['efficiency'],
                                energy_level=item['energy_level'],
                                interruptions=item['interruptions'],
                                task_switches=item['task_switches'],
                                session_duration=item['session_duration'],
                                time_of_day=item['time_of_day'],
                                day_of_week=item['day_of_week']
                            )
                            self.behavioral_data.append(metric)
                        except Exception as e:
                            logger.error(f"Fehler beim Laden Behavioral Data: {e}")
                    
                    logger.info(f"📊 {len(self.behavioral_data)} Analytics-Datenpunkte geladen")
                    
        except Exception as e:
            logger.error(f"Fehler beim Laden historischer Daten: {e}")
    
    def _save_data(self) -> None:
        """Speichert Analytics-Daten"""
        try:
            data_file = self.data_dir / 'analytics_data.json'
            
            # Behavioral Data für Speicherung vorbereiten
            behavioral_data = []
            for metric in list(self.behavioral_data)[-100:]:  # Letzte 100 Einträge
                behavioral_data.append({
                    'timestamp': metric.timestamp.isoformat(),
                    'context': metric.context,
                    'focus_score': metric.focus_score,
                    'efficiency': metric.efficiency,
                    'energy_level': metric.energy_level,
                    'interruptions': metric.interruptions,
                    'task_switches': metric.task_switches,
                    'session_duration': metric.session_duration,
                    'time_of_day': metric.time_of_day,
                    'day_of_week': metric.day_of_week
                })
            
            data = {
                'behavioral_data': behavioral_data,
                'patterns': {pid: asdict(pattern) for pid, pattern in self.productivity_patterns.items()},
                'last_updated': datetime.now().isoformat()
            }
            
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Fehler beim Speichern Analytics-Daten: {e}")

if __name__ == "__main__":
    # Test der Analytics Engine
    analytics = DeepAnalyticsEngine()
    
    # Test-Daten hinzufügen
    import random
    for i in range(20):
        analytics.add_behavioral_data(
            context=random.choice(['programming', 'writing', 'research']),
            focus_score=random.uniform(60, 95),
            efficiency=random.uniform(50, 90),
            energy_level=random.uniform(40, 100),
            interruptions=random.randint(0, 5),
            session_duration=random.uniform(15, 120)
        )
    
    # Dashboard anzeigen
    dashboard = analytics.get_analytics_dashboard()
    print("Analytics Dashboard:", json.dumps(dashboard, indent=2, default=str))
