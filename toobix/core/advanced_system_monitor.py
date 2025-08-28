"""
Toobix Advanced System Monitor
Erweiterte System-Überwachung mit Real-time Performance Analytics
"""

import psutil
import time
import json
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import logging

class AdvancedSystemMonitor:
    """Erweiterte System-Überwachung mit intelligenten Alerts"""
    
    def __init__(self, settings=None):
        self.settings = settings
        self.monitoring_active = False
        self.performance_history = []
        self.alerts_active = True
        self.thresholds = {
            'cpu_warning': 80.0,
            'cpu_critical': 95.0,
            'memory_warning': 85.0,
            'memory_critical': 95.0,
            'disk_warning': 85.0,
            'disk_critical': 95.0,
            'temperature_warning': 70.0,
            'temperature_critical': 85.0
        }
        
        # Performance-Tracking
        self.process_watch_list = []
        self.suspicious_processes = []
        self.startup_programs = []
        
        # Logging
        self.logger = logging.getLogger('AdvancedSystemMonitor')
        
    def start_monitoring(self, interval: int = 5) -> None:
        """Startet kontinuierliche System-Überwachung"""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, 
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info("Advanced System Monitoring gestartet")
    
    def stop_monitoring(self) -> None:
        """Stoppt System-Überwachung"""
        self.monitoring_active = False
        self.logger.info("Advanced System Monitoring gestoppt")
    
    def _monitoring_loop(self, interval: int) -> None:
        """Haupt-Monitoring-Loop"""
        while self.monitoring_active:
            try:
                # System-Metriken sammeln
                metrics = self.collect_system_metrics()
                
                # Performance-Historie aktualisieren
                self.update_performance_history(metrics)
                
                # Alerts prüfen
                if self.alerts_active:
                    self.check_performance_alerts(metrics)
                
                # Verdächtige Prozesse prüfen
                self.analyze_processes()
                
                time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Fehler im Monitoring-Loop: {e}")
                time.sleep(interval)
    
    def collect_system_metrics(self) -> Dict:
        """Sammelt umfassende System-Metriken"""
        try:
            # CPU-Metriken
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()
            
            # Memory-Metriken
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk-Metriken
            disk_usage = {}
            disk_io = psutil.disk_io_counters()
            
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_usage[partition.device] = {
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': (usage.used / usage.total) * 100
                    }
                except PermissionError:
                    continue
            
            # Netzwerk-Metriken
            network = psutil.net_io_counters()
            network_connections = len(psutil.net_connections())
            
            # Prozess-Metriken
            process_count = len(psutil.pids())
            
            # Boot-Zeit
            boot_time = psutil.boot_time()
            uptime = datetime.now() - datetime.fromtimestamp(boot_time)
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'per_core': cpu_per_core,
                    'frequency': {
                        'current': cpu_freq.current if cpu_freq else None,
                        'min': cpu_freq.min if cpu_freq else None,
                        'max': cpu_freq.max if cpu_freq else None
                    },
                    'count': cpu_count
                },
                'memory': {
                    'total': memory.total,
                    'available': memory.available,
                    'used': memory.used,
                    'percent': memory.percent,
                    'swap_total': swap.total,
                    'swap_used': swap.used,
                    'swap_percent': swap.percent
                },
                'disk': {
                    'usage': disk_usage,
                    'io': {
                        'read_count': disk_io.read_count if disk_io else 0,
                        'write_count': disk_io.write_count if disk_io else 0,
                        'read_bytes': disk_io.read_bytes if disk_io else 0,
                        'write_bytes': disk_io.write_bytes if disk_io else 0
                    }
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv,
                    'connections': network_connections
                },
                'system': {
                    'process_count': process_count,
                    'uptime_seconds': uptime.total_seconds(),
                    'boot_time': boot_time
                }
            }
            
        except Exception as e:
            self.logger.error(f"Fehler beim Sammeln der System-Metriken: {e}")
            return {}
    
    def update_performance_history(self, metrics: Dict) -> None:
        """Aktualisiert Performance-Historie"""
        self.performance_history.append(metrics)
        
        # Historie auf letzte 1000 Einträge begrenzen
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]
    
    def check_performance_alerts(self, metrics: Dict) -> List[Dict]:
        """Prüft auf Performance-Probleme und erstellt Alerts"""
        alerts = []
        
        try:
            # CPU-Alerts
            cpu_percent = metrics.get('cpu', {}).get('percent', 0)
            if cpu_percent >= self.thresholds['cpu_critical']:
                alerts.append({
                    'type': 'CRITICAL',
                    'category': 'CPU',
                    'message': f'Kritische CPU-Auslastung: {cpu_percent:.1f}%',
                    'value': cpu_percent,
                    'threshold': self.thresholds['cpu_critical']
                })
            elif cpu_percent >= self.thresholds['cpu_warning']:
                alerts.append({
                    'type': 'WARNING',
                    'category': 'CPU',
                    'message': f'Hohe CPU-Auslastung: {cpu_percent:.1f}%',
                    'value': cpu_percent,
                    'threshold': self.thresholds['cpu_warning']
                })
            
            # Memory-Alerts
            memory_percent = metrics.get('memory', {}).get('percent', 0)
            if memory_percent >= self.thresholds['memory_critical']:
                alerts.append({
                    'type': 'CRITICAL',
                    'category': 'MEMORY',
                    'message': f'Kritischer Speicherverbrauch: {memory_percent:.1f}%',
                    'value': memory_percent,
                    'threshold': self.thresholds['memory_critical']
                })
            elif memory_percent >= self.thresholds['memory_warning']:
                alerts.append({
                    'type': 'WARNING',
                    'category': 'MEMORY',
                    'message': f'Hoher Speicherverbrauch: {memory_percent:.1f}%',
                    'value': memory_percent,
                    'threshold': self.thresholds['memory_warning']
                })
            
            # Disk-Alerts
            disk_usage = metrics.get('disk', {}).get('usage', {})
            for device, usage in disk_usage.items():
                disk_percent = usage.get('percent', 0)
                if disk_percent >= self.thresholds['disk_critical']:
                    alerts.append({
                        'type': 'CRITICAL',
                        'category': 'DISK',
                        'message': f'Kritischer Speicherplatz {device}: {disk_percent:.1f}%',
                        'value': disk_percent,
                        'threshold': self.thresholds['disk_critical'],
                        'device': device
                    })
                elif disk_percent >= self.thresholds['disk_warning']:
                    alerts.append({
                        'type': 'WARNING',
                        'category': 'DISK',
                        'message': f'Wenig Speicherplatz {device}: {disk_percent:.1f}%',
                        'value': disk_percent,
                        'threshold': self.thresholds['disk_warning'],
                        'device': device
                    })
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Fehler beim Prüfen der Performance-Alerts: {e}")
            return []
    
    def analyze_processes(self) -> List[Dict]:
        """Analysiert laufende Prozesse auf Anomalien"""
        suspicious = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'create_time']):
                try:
                    proc_info = proc.info
                    
                    # Hoher CPU-Verbrauch ohne bekannten Grund
                    if proc_info['cpu_percent'] > 50.0:
                        suspicious.append({
                            'type': 'HIGH_CPU',
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cpu_percent': proc_info['cpu_percent'],
                            'memory_percent': proc_info['memory_percent']
                        })
                    
                    # Hoher Speicherverbrauch
                    if proc_info['memory_percent'] > 20.0:
                        suspicious.append({
                            'type': 'HIGH_MEMORY',
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'cpu_percent': proc_info['cpu_percent'],
                            'memory_percent': proc_info['memory_percent']
                        })
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            self.suspicious_processes = suspicious
            return suspicious
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Prozess-Analyse: {e}")
            return []
    
    def get_system_health_score(self) -> Dict:
        """Berechnet System-Gesundheitsscore"""
        try:
            if not self.performance_history:
                return {'score': 100, 'status': 'UNKNOWN', 'details': 'Keine Daten verfügbar'}
            
            latest = self.performance_history[-1]
            
            # Score-Berechnung
            cpu_score = max(0, 100 - latest.get('cpu', {}).get('percent', 0))
            memory_score = max(0, 100 - latest.get('memory', {}).get('percent', 0))
            
            # Disk-Score (schlechteste Partition)
            disk_usage = latest.get('disk', {}).get('usage', {})
            disk_scores = [max(0, 100 - usage.get('percent', 0)) for usage in disk_usage.values()]
            disk_score = min(disk_scores) if disk_scores else 100
            
            # Gewichteter Gesamtscore
            total_score = (cpu_score * 0.4 + memory_score * 0.4 + disk_score * 0.2)
            
            # Status bestimmen
            if total_score >= 90:
                status = 'EXCELLENT'
            elif total_score >= 75:
                status = 'GOOD'
            elif total_score >= 60:
                status = 'WARNING'
            else:
                status = 'CRITICAL'
            
            return {
                'score': round(total_score, 1),
                'status': status,
                'details': {
                    'cpu_score': round(cpu_score, 1),
                    'memory_score': round(memory_score, 1),
                    'disk_score': round(disk_score, 1)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Fehler bei der Health-Score-Berechnung: {e}")
            return {'score': 0, 'status': 'ERROR', 'details': str(e)}
    
    def get_startup_programs(self) -> List[Dict]:
        """Ermittelt Autostart-Programme"""
        try:
            startup_programs = []
            
            # Windows Registry für Autostart-Programme lesen
            import winreg
            
            # HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run") as key:
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_programs.append({
                                'name': name,
                                'path': value,
                                'location': 'HKCU\\Run',
                                'enabled': True
                            })
                            i += 1
                        except WindowsError:
                            break
            except Exception:
                pass
            
            # HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run") as key:
                    i = 0
                    while True:
                        try:
                            name, value, _ = winreg.EnumValue(key, i)
                            startup_programs.append({
                                'name': name,
                                'path': value,
                                'location': 'HKLM\\Run',
                                'enabled': True
                            })
                            i += 1
                        except WindowsError:
                            break
            except Exception:
                pass
            
            self.startup_programs = startup_programs
            return startup_programs
            
        except Exception as e:
            self.logger.error(f"Fehler beim Ermitteln der Autostart-Programme: {e}")
            return []
    
    def get_network_connections(self) -> List[Dict]:
        """Ermittelt aktive Netzwerk-Verbindungen"""
        try:
            connections = []
            
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == psutil.CONN_ESTABLISHED:
                    try:
                        proc = psutil.Process(conn.pid) if conn.pid else None
                        connections.append({
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                            'status': conn.status,
                            'pid': conn.pid,
                            'process_name': proc.name() if proc else 'Unknown'
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        connections.append({
                            'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                            'remote_address': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                            'status': conn.status,
                            'pid': conn.pid,
                            'process_name': 'Access Denied'
                        })
            
            return connections
            
        except Exception as e:
            self.logger.error(f"Fehler beim Ermitteln der Netzwerk-Verbindungen: {e}")
            return []
    
    def get_performance_report(self) -> Dict:
        """Erstellt umfassenden Performance-Report"""
        try:
            current_metrics = self.collect_system_metrics()
            health_score = self.get_system_health_score()
            startup_programs = self.get_startup_programs()
            network_connections = self.get_network_connections()
            
            # Trend-Analyse der letzten 10 Messungen
            recent_history = self.performance_history[-10:] if len(self.performance_history) >= 10 else self.performance_history
            
            cpu_trend = []
            memory_trend = []
            
            for entry in recent_history:
                cpu_trend.append(entry.get('cpu', {}).get('percent', 0))
                memory_trend.append(entry.get('memory', {}).get('percent', 0))
            
            # Durchschnittswerte
            avg_cpu = sum(cpu_trend) / len(cpu_trend) if cpu_trend else 0
            avg_memory = sum(memory_trend) / len(memory_trend) if memory_trend else 0
            
            return {
                'report_time': datetime.now().isoformat(),
                'health_score': health_score,
                'current_metrics': current_metrics,
                'trends': {
                    'cpu_average': round(avg_cpu, 1),
                    'memory_average': round(avg_memory, 1),
                    'cpu_history': cpu_trend,
                    'memory_history': memory_trend
                },
                'startup_programs': {
                    'count': len(startup_programs),
                    'programs': startup_programs
                },
                'network': {
                    'active_connections': len(network_connections),
                    'connections': network_connections[:10]  # Top 10
                },
                'suspicious_processes': self.suspicious_processes,
                'recommendations': self._generate_recommendations(current_metrics, health_score)
            }
            
        except Exception as e:
            self.logger.error(f"Fehler beim Erstellen des Performance-Reports: {e}")
            return {'error': str(e)}
    
    def _generate_recommendations(self, metrics: Dict, health_score: Dict) -> List[str]:
        """Generiert Optimierungs-Empfehlungen"""
        recommendations = []
        
        try:
            # CPU-Empfehlungen
            cpu_percent = metrics.get('cpu', {}).get('percent', 0)
            if cpu_percent > 80:
                recommendations.append("🔥 CPU-Auslastung kritisch - Schließe nicht benötigte Programme")
            
            # Memory-Empfehlungen
            memory_percent = metrics.get('memory', {}).get('percent', 0)
            if memory_percent > 85:
                recommendations.append("💾 Speicher fast voll - Beende speicherhungrige Anwendungen")
            
            # Disk-Empfehlungen
            disk_usage = metrics.get('disk', {}).get('usage', {})
            for device, usage in disk_usage.items():
                if usage.get('percent', 0) > 90:
                    recommendations.append(f"💽 Festplatte {device} fast voll - Dateien aufräumen empfohlen")
            
            # Autostart-Empfehlungen
            if len(self.startup_programs) > 10:
                recommendations.append("🚀 Viele Autostart-Programme - Deaktiviere nicht benötigte")
            
            # Allgemeine Empfehlungen
            if health_score.get('score', 100) < 75:
                recommendations.append("⚠️ System-Performance suboptimal - Neustart empfohlen")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Fehler beim Generieren der Empfehlungen: {e}")
            return ["Fehler beim Generieren der Empfehlungen"]
