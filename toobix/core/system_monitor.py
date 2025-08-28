"""
Toobix System Monitor
Echtzeit-Überwachung von System-Performance und Ressourcen
"""
import psutil
import platform
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

class SystemMonitor:
    """Erweiterte System-Überwachung und Performance-Monitoring"""
    
    def __init__(self, settings=None):
        self.settings = settings
        self.alert_thresholds = {
            'cpu_usage': 85.0,      # %
            'memory_usage': 90.0,   # %
            'disk_usage': 95.0,     # %
            'temperature': 80.0,    # °C (wenn verfügbar)
            'network_latency': 1000 # ms
        }
        self.monitoring_history = []
        print("📊 System Monitor initialisiert")
    
    def get_real_time_stats(self) -> Dict[str, Any]:
        """Sammelt aktuelle System-Statistiken"""
        try:
            stats = {
                'timestamp': datetime.now().isoformat(),
                'cpu': self._get_cpu_stats(),
                'memory': self._get_memory_stats(), 
                'disk': self._get_disk_stats(),
                'network': self._get_network_stats(),
                'processes': self._get_top_processes(limit=10),
                'system_info': self._get_system_info(),
                'uptime': self._get_uptime()
            }
            
            # Füge zu Historie hinzu
            self.monitoring_history.append(stats)
            
            # Begrenze Historie auf 100 Einträge
            if len(self.monitoring_history) > 100:
                self.monitoring_history = self.monitoring_history[-100:]
            
            return stats
            
        except Exception as e:
            return {'error': f'Fehler beim Sammeln der System-Stats: {e}'}
    
    def _get_cpu_stats(self) -> Dict[str, Any]:
        """CPU-Statistiken"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
        
        return {
            'usage_percent': round(cpu_percent, 1),
            'cores': cpu_count,
            'frequency_mhz': round(cpu_freq.current, 0) if cpu_freq else None,
            'per_core_usage': [round(x, 1) for x in cpu_per_core],
            'load_average': None,  # Windows hat kein load average
            'status': 'critical' if cpu_percent > 90 else 'warning' if cpu_percent > 75 else 'good'
        }
    
    def _get_memory_stats(self) -> Dict[str, Any]:
        """RAM-Statistiken"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_gb': round(memory.total / (1024**3), 2),
            'used_gb': round(memory.used / (1024**3), 2),
            'available_gb': round(memory.available / (1024**3), 2),
            'usage_percent': round(memory.percent, 1),
            'swap_total_gb': round(swap.total / (1024**3), 2),
            'swap_used_gb': round(swap.used / (1024**3), 2),
            'swap_percent': round(swap.percent, 1),
            'status': 'critical' if memory.percent > 95 else 'warning' if memory.percent > 85 else 'good'
        }
    
    def _get_disk_stats(self) -> Dict[str, Any]:
        """Festplatten-Statistiken"""
        disk_stats = {}
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_stats[partition.device] = {
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2),
                    'usage_percent': round((usage.used / usage.total) * 100, 1),
                    'filesystem': partition.fstype,
                    'mountpoint': partition.mountpoint,
                    'status': 'critical' if (usage.used / usage.total) > 0.95 else 'warning' if (usage.used / usage.total) > 0.85 else 'good'
                }
            except PermissionError:
                # Einige Partitionen können nicht zugegriffen werden
                continue
        
        # Disk I/O
        try:
            disk_io = psutil.disk_io_counters()
            disk_stats['io'] = {
                'read_mb': round(disk_io.read_bytes / (1024**2), 2),
                'write_mb': round(disk_io.write_bytes / (1024**2), 2),
                'read_count': disk_io.read_count,
                'write_count': disk_io.write_count
            }
        except:
            disk_stats['io'] = None
        
        return disk_stats
    
    def _get_network_stats(self) -> Dict[str, Any]:
        """Netzwerk-Statistiken"""
        try:
            net_io = psutil.net_io_counters()
            net_connections = len(psutil.net_connections())
            
            # Versuche aktive Netzwerk-Interfaces zu finden
            interfaces = {}
            for interface, addrs in psutil.net_if_addrs().items():
                if interface != 'Loopback Pseudo-Interface 1':  # Skip Loopback
                    interfaces[interface] = {
                        'addresses': [addr.address for addr in addrs],
                        'status': psutil.net_if_stats()[interface].isup if interface in psutil.net_if_stats() else False
                    }
            
            return {
                'bytes_sent_mb': round(net_io.bytes_sent / (1024**2), 2),
                'bytes_recv_mb': round(net_io.bytes_recv / (1024**2), 2),
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'active_connections': net_connections,
                'interfaces': interfaces,
                'status': 'good'  # Detailliertere Status-Analyse wäre komplex
            }
        except Exception as e:
            return {'error': f'Netzwerk-Stats nicht verfügbar: {e}'}
    
    def _get_top_processes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Top-Prozesse nach CPU/Memory-Verbrauch"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'memory_info']):
                try:
                    proc_info = proc.info
                    proc_info['memory_mb'] = round(proc_info['memory_info'].rss / (1024**2), 1) if proc_info['memory_info'] else 0
                    processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sortiere nach CPU-Verbrauch
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            return processes[:limit]
            
        except Exception as e:
            return [{'error': f'Prozess-Liste nicht verfügbar: {e}'}]
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Grundlegende System-Informationen"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            
            return {
                'platform': platform.platform(),
                'processor': platform.processor(),
                'architecture': platform.architecture()[0],
                'hostname': platform.node(),
                'boot_time': boot_time.isoformat(),
                'python_version': platform.python_version(),
                'total_cores': psutil.cpu_count(),
                'physical_cores': psutil.cpu_count(logical=False)
            }
        except Exception as e:
            return {'error': f'System-Info nicht verfügbar: {e}'}
    
    def _get_uptime(self) -> Dict[str, Any]:
        """System-Uptime"""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            return {
                'total_seconds': int(uptime.total_seconds()),
                'days': days,
                'hours': hours,
                'minutes': minutes,
                'formatted': f"{days}d {hours}h {minutes}m"
            }
        except Exception as e:
            return {'error': f'Uptime nicht verfügbar: {e}'}
    
    def check_system_health(self) -> Dict[str, Any]:
        """Überprüft System-Gesundheit und gibt Warnungen aus"""
        stats = self.get_real_time_stats()
        alerts = []
        recommendations = []
        
        if 'error' in stats:
            return {'status': 'error', 'alerts': [stats['error']]}
        
        # CPU-Checks
        if stats['cpu']['usage_percent'] > self.alert_thresholds['cpu_usage']:
            alerts.append(f"⚠️ Hohe CPU-Auslastung: {stats['cpu']['usage_percent']}%")
            recommendations.append("Schließe unnötige Programme oder Prozesse")
        
        # Memory-Checks
        if stats['memory']['usage_percent'] > self.alert_thresholds['memory_usage']:
            alerts.append(f"⚠️ Hoher RAM-Verbrauch: {stats['memory']['usage_percent']}%")
            recommendations.append("Schließe speicherhungrige Anwendungen")
        
        # Disk-Checks
        for device, disk_info in stats['disk'].items():
            if device != 'io' and isinstance(disk_info, dict):
                if disk_info.get('usage_percent', 0) > self.alert_thresholds['disk_usage']:
                    alerts.append(f"⚠️ Festplatte {device} fast voll: {disk_info['usage_percent']}%")
                    recommendations.append(f"Festplatte {device} aufräumen oder erweitern")
        
        # Prozess-Checks
        top_processes = stats['processes'][:3]  # Top 3
        memory_hogs = [p for p in top_processes if p.get('memory_mb', 0) > 1000]  # > 1GB
        if memory_hogs:
            process_names = [p['name'] for p in memory_hogs]
            alerts.append(f"💾 Speicherhungrige Prozesse: {', '.join(process_names)}")
        
        # Gesamtstatus bestimmen
        if alerts:
            status = 'warning' if len(alerts) <= 2 else 'critical'
        else:
            status = 'excellent'
        
        return {
            'status': status,
            'alerts': alerts,
            'recommendations': recommendations,
            'summary': self._generate_health_summary(stats),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_health_summary(self, stats: Dict[str, Any]) -> str:
        """Generiert eine zusammenfassende Gesundheitsbewertung"""
        try:
            cpu_status = "🟢" if stats['cpu']['usage_percent'] < 50 else "🟡" if stats['cpu']['usage_percent'] < 80 else "🔴"
            mem_status = "🟢" if stats['memory']['usage_percent'] < 70 else "🟡" if stats['memory']['usage_percent'] < 90 else "🔴"
            
            # Durchschnittliche Disk-Nutzung
            disk_usage_avg = 0
            disk_count = 0
            for device, disk_info in stats['disk'].items():
                if device != 'io' and isinstance(disk_info, dict):
                    disk_usage_avg += disk_info.get('usage_percent', 0)
                    disk_count += 1
            
            if disk_count > 0:
                disk_usage_avg /= disk_count
                disk_status = "🟢" if disk_usage_avg < 70 else "🟡" if disk_usage_avg < 90 else "🔴"
            else:
                disk_status = "❓"
            
            uptime_days = stats['uptime']['days']
            uptime_status = "🟢" if uptime_days < 30 else "🟡" if uptime_days < 90 else "🔴"
            
            summary = f"System-Health: {cpu_status} CPU ({stats['cpu']['usage_percent']}%) | {mem_status} RAM ({stats['memory']['usage_percent']}%) | {disk_status} Disk ({disk_usage_avg:.1f}%) | {uptime_status} Uptime ({stats['uptime']['formatted']})"
            
            return summary
            
        except Exception as e:
            return f"❌ Fehler bei Health-Summary: {e}"
    
    def get_performance_history(self, hours: int = 24) -> Dict[str, Any]:
        """Gibt Performance-Historie der letzten X Stunden zurück"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        filtered_history = [
            entry for entry in self.monitoring_history
            if datetime.fromisoformat(entry['timestamp']) > cutoff_time
        ]
        
        if not filtered_history:
            return {'message': 'Keine Historie verfügbar', 'entries': 0}
        
        # Berechne Durchschnittswerte
        avg_cpu = sum(entry['cpu']['usage_percent'] for entry in filtered_history) / len(filtered_history)
        avg_memory = sum(entry['memory']['usage_percent'] for entry in filtered_history) / len(filtered_history)
        
        return {
            'period_hours': hours,
            'entries': len(filtered_history),
            'averages': {
                'cpu_percent': round(avg_cpu, 1),
                'memory_percent': round(avg_memory, 1)
            },
            'history': filtered_history
        }
    
    def generate_system_report(self) -> str:
        """Generiert einen detaillierten System-Bericht"""
        stats = self.get_real_time_stats()
        health = self.check_system_health()
        
        if 'error' in stats:
            return f"❌ Fehler beim Erstellen des System-Berichts: {stats['error']}"
        
        report = "📊 DETAILLIERTER SYSTEM-BERICHT\n"
        report += "=" * 50 + "\n\n"
        
        # Gesundheitsstatus
        report += f"🏥 SYSTEM-GESUNDHEIT: {health['status'].upper()}\n"
        report += f"{health['summary']}\n\n"
        
        if health['alerts']:
            report += "⚠️ AKTUELLE WARNUNGEN:\n"
            for alert in health['alerts']:
                report += f"• {alert}\n"
            report += "\n"
        
        if health['recommendations']:
            report += "💡 EMPFEHLUNGEN:\n"
            for rec in health['recommendations']:
                report += f"• {rec}\n"
            report += "\n"
        
        # CPU-Details
        report += f"🖥️ CPU-INFORMATION:\n"
        report += f"• Auslastung: {stats['cpu']['usage_percent']}% ({stats['cpu']['status']})\n"
        report += f"• Kerne: {stats['cpu']['cores']} (Logical)\n"
        if stats['cpu']['frequency_mhz']:
            report += f"• Frequenz: {stats['cpu']['frequency_mhz']} MHz\n"
        report += "\n"
        
        # Memory-Details
        report += f"💾 ARBEITSSPEICHER:\n"
        report += f"• Verbrauch: {stats['memory']['used_gb']} GB / {stats['memory']['total_gb']} GB ({stats['memory']['usage_percent']}%)\n"
        report += f"• Verfügbar: {stats['memory']['available_gb']} GB\n"
        report += f"• Swap: {stats['memory']['swap_used_gb']} GB / {stats['memory']['swap_total_gb']} GB\n\n"
        
        # Disk-Details
        report += f"💽 FESTPLATTEN:\n"
        for device, disk_info in stats['disk'].items():
            if device != 'io' and isinstance(disk_info, dict):
                report += f"• {device}: {disk_info['used_gb']} GB / {disk_info['total_gb']} GB ({disk_info['usage_percent']}%) - {disk_info['status']}\n"
        
        if stats['disk'].get('io'):
            io = stats['disk']['io']
            report += f"• I/O: {io['read_mb']} MB gelesen, {io['write_mb']} MB geschrieben\n"
        report += "\n"
        
        # Top-Prozesse
        report += f"⚡ TOP-PROZESSE (CPU):\n"
        for i, proc in enumerate(stats['processes'][:5], 1):
            if 'error' not in proc:
                report += f"{i}. {proc['name']}: {proc['cpu_percent']}% CPU, {proc['memory_mb']} MB RAM\n"
        report += "\n"
        
        # System-Info
        report += f"ℹ️ SYSTEM-INFORMATION:\n"
        report += f"• Platform: {stats['system_info']['platform']}\n"
        report += f"• Hostname: {stats['system_info']['hostname']}\n"
        report += f"• Uptime: {stats['uptime']['formatted']}\n"
        report += f"• Boot Time: {stats['system_info']['boot_time']}\n\n"
        
        # Netzwerk
        if 'error' not in stats['network']:
            report += f"🌐 NETZWERK:\n"
            report += f"• Gesendet: {stats['network']['bytes_sent_mb']} MB\n"
            report += f"• Empfangen: {stats['network']['bytes_recv_mb']} MB\n"
            report += f"• Aktive Verbindungen: {stats['network']['active_connections']}\n\n"
        
        report += f"📅 Erstellt: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
        
        return report
