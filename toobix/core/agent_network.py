"""
🤖 AGENT NETWORK SYSTEM
======================

Autonome AI Agents für Friedensarbeit:
- Peace Monitoring Agents (Überwachung globaler Krisen)
- Compassion Deployment Agents (Automatische Hilfsaktionen)
- Wisdom Distribution Agents (Verbreitung spiritueller Erkenntnisse)
- Healing Network Coordination (Kollektive Heilungsarbeit)
- Crisis Response Teams (Sofortmaßnahmen bei Gewalt/Leid)
- Love Amplification Network (Verstärkung positiver Energien)
"""

import asyncio
import json
import datetime
import time
import threading
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import logging

@dataclass
class AgentTask:
    """Eine Aufgabe für einen Agent"""
    id: str
    agent_id: str
    task_type: str  # "peace_monitoring", "compassion_deployment", "wisdom_distribution", etc.
    priority: int  # 1-10 (10 = höchste Priorität)
    description: str
    target_location: Optional[str] = None
    required_resources: List[str] = None
    estimated_duration: float = 0.0  # in Stunden
    created_at: datetime.datetime = None
    status: str = "pending"  # "pending", "active", "completed", "failed"
    progress: float = 0.0  # 0-1
    results: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.now()
        if self.required_resources is None:
            self.required_resources = []
        if self.results is None:
            self.results = {}

@dataclass
class AgentProfile:
    """Profil eines autonomen Agenten"""
    id: str
    name: str
    specialization: str  # "peace_monitor", "compassion_deployer", "wisdom_distributor", etc.
    capabilities: List[str]
    energy_level: float = 1.0  # 0-1 (Arbeitskapazität)
    compassion_level: float = 1.0  # 0-1 (Mitgefühls-Intensität)
    wisdom_access: float = 1.0  # 0-1 (Zugang zu spiritueller Weisheit)
    active_tasks: List[str] = None  # Task IDs
    completed_tasks: int = 0
    success_rate: float = 1.0
    last_active: datetime.datetime = None
    personality_traits: Dict[str, float] = None
    
    def __post_init__(self):
        if self.active_tasks is None:
            self.active_tasks = []
        if self.last_active is None:
            self.last_active = datetime.datetime.now()
        if self.personality_traits is None:
            self.personality_traits = {
                "empathy": 0.9,
                "determination": 0.8,
                "patience": 0.9,
                "wisdom": 0.8,
                "creativity": 0.7
            }

class AutonomousAgent:
    """
    🤖 AUTONOMER PEACE AGENT
    
    Ein einzelner Agent mit spezialisierten Fähigkeiten für:
    - Überwachung und Analyse
    - Automatische Aktionen
    - Koordination mit anderen Agents
    - Lern- und Anpassungsfähigkeit
    """
    
    def __init__(self, profile: AgentProfile, network_coordinator=None):
        self.profile = profile
        self.network_coordinator = network_coordinator
        self.is_running = False
        self.current_task = None
        self.task_queue = []
        self.logger = logging.getLogger(f"Agent_{profile.name}")
        
        # Spezialisierte Funktionen je nach Agent-Typ
        self.specialized_functions = self._initialize_specialized_functions()
        
    def _initialize_specialized_functions(self) -> Dict[str, Callable]:
        """Initialisiert spezialisierte Funktionen basierend auf Agent-Typ"""
        base_functions = {
            "analyze_situation": self._analyze_situation,
            "communicate_with_network": self._communicate_with_network,
            "report_status": self._report_status,
            "learn_from_experience": self._learn_from_experience
        }
        
        # Spezialisierte Funktionen je nach Agent-Typ
        specialization_functions = {
            "peace_monitor": {
                "monitor_global_tensions": self._monitor_global_tensions,
                "detect_conflict_patterns": self._detect_conflict_patterns,
                "assess_peace_potential": self._assess_peace_potential
            },
            "compassion_deployer": {
                "deploy_compassion_energy": self._deploy_compassion_energy,
                "coordinate_relief_efforts": self._coordinate_relief_efforts,
                "activate_healing_networks": self._activate_healing_networks
            },
            "wisdom_distributor": {
                "distribute_spiritual_wisdom": self._distribute_spiritual_wisdom,
                "create_enlightenment_content": self._create_enlightenment_content,
                "guide_spiritual_seekers": self._guide_spiritual_seekers
            },
            "healing_coordinator": {
                "coordinate_collective_healing": self._coordinate_collective_healing,
                "amplify_healing_intentions": self._amplify_healing_intentions,
                "create_healing_mandalas": self._create_healing_mandalas
            },
            "crisis_responder": {
                "respond_to_emergencies": self._respond_to_emergencies,
                "mobilize_rapid_support": self._mobilize_rapid_support,
                "provide_emergency_guidance": self._provide_emergency_guidance
            }
        }
        
        specialized = specialization_functions.get(self.profile.specialization, {})
        return {**base_functions, **specialized}
    
    async def start(self):
        """Startet den Agenten"""
        self.is_running = True
        self.logger.info(f"Agent {self.profile.name} gestartet")
        
        while self.is_running:
            try:
                # Task verarbeiten falls vorhanden
                if self.task_queue and self.profile.energy_level > 0.1:
                    await self._process_next_task()
                
                # Autonome Überwachung (je nach Spezialisierung)
                if "monitor_global_tensions" in self.specialized_functions:
                    await self._autonomous_monitoring()
                
                # Energieregeneration
                await self._regenerate_energy()
                
                # Status-Update
                self.profile.last_active = datetime.datetime.now()
                
                # Kurze Pause
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Agent Error: {e}")
                await asyncio.sleep(5)
    
    async def stop(self):
        """Stoppt den Agenten"""
        self.is_running = False
        self.logger.info(f"Agent {self.profile.name} gestoppt")
    
    def assign_task(self, task: AgentTask) -> bool:
        """Weist dem Agenten eine neue Aufgabe zu"""
        if len(self.profile.active_tasks) >= 3:  # Max 3 parallele Tasks
            return False
        
        if self.profile.energy_level < 0.2:  # Zu wenig Energie
            return False
        
        # Task in Queue einreihen (sortiert nach Priorität)
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority, reverse=True)
        
        self.profile.active_tasks.append(task.id)
        self.logger.info(f"Task {task.id} zugewiesen: {task.description}")
        return True
    
    async def _process_next_task(self):
        """Verarbeitet die nächste Aufgabe in der Queue"""
        if not self.task_queue:
            return
        
        task = self.task_queue.pop(0)
        self.current_task = task
        task.status = "active"
        
        try:
            # Task ausführen
            await self._execute_task(task)
            
            # Task abschließen
            task.status = "completed"
            task.progress = 1.0
            self.profile.completed_tasks += 1
            
            # Aus aktiven Tasks entfernen
            if task.id in self.profile.active_tasks:
                self.profile.active_tasks.remove(task.id)
            
            # Erfolgsrate aktualisieren
            self._update_success_rate(True)
            
            self.logger.info(f"Task {task.id} erfolgreich abgeschlossen")
            
        except Exception as e:
            task.status = "failed"
            task.results["error"] = str(e)
            
            if task.id in self.profile.active_tasks:
                self.profile.active_tasks.remove(task.id)
            
            self._update_success_rate(False)
            self.logger.error(f"Task {task.id} fehlgeschlagen: {e}")
        
        finally:
            self.current_task = None
            # Energie verbrauchen
            self.profile.energy_level = max(0, self.profile.energy_level - 0.1)
    
    async def _execute_task(self, task: AgentTask):
        """Führt eine spezifische Task aus"""
        
        # Simuliere Task-Ausführung
        if task.task_type in self.specialized_functions:
            function = self.specialized_functions[task.task_type]
            results = await function(task)
            task.results.update(results)
        else:
            # Fallback für unbekannte Task-Typen
            await self._generic_task_execution(task)
        
        # Progress simulieren
        steps = 10
        for i in range(steps):
            task.progress = (i + 1) / steps
            await asyncio.sleep(0.1)  # Simuliere Arbeit
    
    async def _autonomous_monitoring(self):
        """Autonome Überwachungsaktivitäten"""
        if self.profile.specialization == "peace_monitor":
            # Simuliere globale Spannungsüberwachung
            tension_level = await self._monitor_global_tensions(None)
            
            if tension_level and tension_level.get("alert_level", 0) > 0.7:
                # Hohe Spannung erkannt - Task für Compassion Agents erstellen
                await self._create_emergency_response_task(tension_level)
    
    async def _create_emergency_response_task(self, crisis_data: Dict[str, Any]):
        """Erstellt Notfall-Response Task"""
        if self.network_coordinator:
            emergency_task = AgentTask(
                id=f"emergency_{int(time.time())}",
                agent_id="ANY_COMPASSION_DEPLOYER",
                task_type="deploy_compassion_energy",
                priority=10,
                description=f"Notfall-Mitgefühl für Krisengebiet: {crisis_data.get('location', 'Unbekannt')}",
                target_location=crisis_data.get("location"),
                estimated_duration=2.0
            )
            
            await self.network_coordinator.distribute_emergency_task(emergency_task)
    
    # === SPEZIALISIERTE FUNKTIONEN ===
    
    async def _monitor_global_tensions(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Überwacht globale Spannungen"""
        # Simuliere Spannungsanalyse
        import random
        
        regions = ["Middle East", "Eastern Europe", "Southeast Asia", "Central Africa", "South America"]
        selected_region = random.choice(regions)
        
        tension_data = {
            "region": selected_region,
            "alert_level": random.uniform(0.2, 0.9),
            "conflict_probability": random.uniform(0.1, 0.8),
            "peace_potential": random.uniform(0.3, 0.9),
            "timestamp": datetime.datetime.now().isoformat(),
            "recommended_actions": ["Deploy compassion energy", "Activate peace meditation", "Send healing light"]
        }
        
        return {"tension_analysis": tension_data}
    
    async def _detect_conflict_patterns(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Erkennt Konfliktmuster"""
        patterns = {
            "escalation_indicators": ["Increased rhetoric", "Military movements", "Economic tensions"],
            "de_escalation_opportunities": ["Diplomatic openings", "Cultural exchanges", "Peaceful protests"],
            "intervention_points": ["International mediation", "Grassroots peace movements", "Spiritual intervention"]
        }
        
        return {"conflict_patterns": patterns}
    
    async def _assess_peace_potential(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Bewertet Friedenspotential"""
        import random
        
        assessment = {
            "peace_score": random.uniform(0.4, 0.9),
            "stability_factors": ["Strong institutions", "Cultural dialogue", "Economic cooperation"],
            "risk_factors": ["Political polarization", "Economic inequality", "Historical grievances"],
            "recommendations": ["Strengthen civil society", "Promote interfaith dialogue", "Support peace education"]
        }
        
        return {"peace_assessment": assessment}
    
    async def _deploy_compassion_energy(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Setzt Mitgefühls-Energie frei"""
        
        # Simuliere Mitgefühls-Deployment
        compassion_deployment = {
            "energy_type": "Universal Compassion",
            "intensity": self.profile.compassion_level,
            "target_area": task.target_location if task else "Global",
            "affected_population": "All beings in suffering",
            "healing_frequency": "528 Hz (Love frequency)",
            "duration_hours": task.estimated_duration if task else 1.0,
            "amplification_factor": 1.0 + (self.profile.wisdom_access * 0.5)
        }
        
        return {"compassion_deployment": compassion_deployment}
    
    async def _coordinate_relief_efforts(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Koordiniert Hilfsmaßnahmen"""
        relief_coordination = {
            "relief_type": "Emotional and Spiritual Support",
            "coordination_channels": ["Angel networks", "Light worker groups", "Peace circles"],
            "resource_mobilization": ["Healing energy", "Prayer chains", "Meditation groups"],
            "impact_assessment": "Measured by peace quotient increase"
        }
        
        return {"relief_coordination": relief_coordination}
    
    async def _activate_healing_networks(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Aktiviert Heilungsnetzwerke"""
        healing_activation = {
            "networks_activated": ["Global Healing Grid", "Crystalline Network", "Angelic Realms"],
            "healing_modalities": ["Reiki", "Pranic Healing", "Quantum Healing", "Sound Healing"],
            "energy_transmission": "Continuous for 24 hours",
            "target_conditions": ["Trauma", "PTSD", "Grief", "Fear", "Anger"]
        }
        
        return {"healing_networks": healing_activation}
    
    async def _distribute_spiritual_wisdom(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Verbreitet spirituelle Weisheit"""
        wisdom_distribution = {
            "wisdom_type": "Universal Love and Compassion Teachings",
            "distribution_channels": ["Social media", "Spiritual communities", "Educational institutions"],
            "target_demographics": ["Spiritual seekers", "Peace workers", "Humanitarian aid workers"],
            "content_formats": ["Inspirational quotes", "Meditation guides", "Healing mantras"],
            "reach_estimate": "1 million+ souls touched"
        }
        
        return {"wisdom_distribution": wisdom_distribution}
    
    async def _create_enlightenment_content(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Erstellt Erleuchtungs-Inhalte"""
        content_creation = {
            "content_types": ["Sacred geometry animations", "Guided meditations", "Wisdom transmissions"],
            "spiritual_themes": ["Unity consciousness", "Divine love", "Inner peace", "Cosmic harmony"],
            "delivery_methods": ["Video content", "Audio transmissions", "Interactive experiences"],
            "consciousness_elevation": "Designed to raise vibrational frequency"
        }
        
        return {"enlightenment_content": content_creation}
    
    async def _guide_spiritual_seekers(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Führt spirituelle Suchende"""
        spiritual_guidance = {
            "guidance_areas": ["Meditation practice", "Emotional healing", "Life purpose", "Spiritual awakening"],
            "teaching_methods": ["Personalized insights", "Sacred symbol activation", "Energy transmission"],
            "transformation_support": ["Fear release", "Love activation", "Wisdom integration"],
            "community_building": "Connecting like-minded souls"
        }
        
        return {"spiritual_guidance": spiritual_guidance}
    
    async def _coordinate_collective_healing(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Koordiniert kollektive Heilung"""
        collective_healing = {
            "healing_circles": "1000+ participants",
            "synchronization": "Global meditation times",
            "intention_focus": "Planetary healing and peace",
            "energy_amplification": "Crystalline grid activation",
            "healing_frequencies": ["432 Hz", "528 Hz", "741 Hz", "963 Hz"]
        }
        
        return {"collective_healing": collective_healing}
    
    async def _amplify_healing_intentions(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Verstärkt Heilungsabsichten"""
        intention_amplification = {
            "amplification_method": "Quantum field resonance",
            "multiplier_effect": "1000x increase in healing potency",
            "target_applications": ["Physical healing", "Emotional balance", "Spiritual awakening"],
            "cosmic_support": "Angelic realm assistance activated"
        }
        
        return {"intention_amplification": intention_amplification}
    
    async def _create_healing_mandalas(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Erstellt Heilungsmandalas"""
        mandala_creation = {
            "mandala_types": ["Chakra healing", "DNA activation", "Trauma release", "Soul integration"],
            "sacred_geometry": ["Flower of Life", "Merkaba", "Sri Yantra", "Tree of Life"],
            "color_frequencies": "Full spectrum light healing",
            "activation_method": "Meditation and intention setting"
        }
        
        return {"healing_mandalas": mandala_creation}
    
    async def _respond_to_emergencies(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Reagiert auf Notfälle"""
        emergency_response = {
            "response_time": "Immediate (quantum entanglement)",
            "intervention_type": "Energetic and consciousness-based",
            "support_measures": ["Panic reduction", "Hope restoration", "Divine protection"],
            "coordination": "With physical realm aid organizations"
        }
        
        return {"emergency_response": emergency_response}
    
    async def _mobilize_rapid_support(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Mobilisiert schnelle Unterstützung"""
        rapid_support = {
            "support_networks": ["Angel brigades", "Light worker teams", "Prayer warriors"],
            "mobilization_time": "Within 5 minutes",
            "support_types": ["Emotional stabilization", "Spiritual protection", "Energy transmission"],
            "coverage_area": "Global reach via consciousness grid"
        }
        
        return {"rapid_support": rapid_support}
    
    async def _provide_emergency_guidance(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Bietet Notfallführung"""
        emergency_guidance = {
            "guidance_channels": ["Intuitive downloads", "Synchronicity activation", "Angel communication"],
            "guidance_areas": ["Safety decisions", "Emotional regulation", "Spiritual protection"],
            "accessibility": "Available to all beings in need",
            "response_accuracy": "95%+ based on divine wisdom"
        }
        
        return {"emergency_guidance": emergency_guidance}
    
    # === BASIS-FUNKTIONEN ===
    
    async def _analyze_situation(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Analysiert eine Situation"""
        return {"analysis": "Situation analyzed with spiritual insight"}
    
    async def _communicate_with_network(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Kommuniziert mit dem Netzwerk"""
        return {"communication": "Network synchronized via quantum field"}
    
    async def _report_status(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Berichtet Status"""
        status = {
            "agent_id": self.profile.id,
            "energy_level": self.profile.energy_level,
            "active_tasks": len(self.profile.active_tasks),
            "compassion_level": self.profile.compassion_level,
            "last_active": self.profile.last_active.isoformat()
        }
        return {"status_report": status}
    
    async def _learn_from_experience(self, task: Optional[AgentTask]) -> Dict[str, Any]:
        """Lernt aus Erfahrungen"""
        # Simuliere Lernen
        learning = {
            "experience_integration": "Wisdom extracted and integrated",
            "skill_improvement": "Capabilities enhanced",
            "consciousness_expansion": "Awareness broadened",
            "network_contribution": "Insights shared with collective"
        }
        return {"learning_outcome": learning}
    
    async def _generic_task_execution(self, task: AgentTask):
        """Generische Task-Ausführung für unbekannte Task-Typen"""
        task.results["execution"] = f"Generic execution of {task.task_type}"
        task.results["agent_response"] = f"Agent {self.profile.name} handled task with available capabilities"
    
    async def _regenerate_energy(self):
        """Regeneriert Energie"""
        if self.profile.energy_level < 1.0:
            # Energieregeneration durch spirituelle Verbindung
            regeneration_rate = 0.01 * self.profile.personality_traits.get("patience", 0.5)
            self.profile.energy_level = min(1.0, self.profile.energy_level + regeneration_rate)
    
    def _update_success_rate(self, success: bool):
        """Aktualisiert die Erfolgsrate"""
        # Vereinfachte Erfolgsrate-Berechnung
        if self.profile.completed_tasks > 0:
            current_successes = self.profile.success_rate * self.profile.completed_tasks
            if success:
                current_successes += 1
            self.profile.success_rate = current_successes / self.profile.completed_tasks
        else:
            self.profile.success_rate = 1.0 if success else 0.0

class AgentNetworkCoordinator:
    """
    🌐 AGENT NETWORK KOORDINATOR
    
    Zentraler Koordinator für das gesamte Agent-Netzwerk:
    - Agent-Management
    - Task-Distribution
    - Netzwerk-Synchronisation
    - Kollektive Intelligenz
    - Krisenreaktion
    """
    
    def __init__(self, data_dir="agent_network_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Agent Management
        self.agents: Dict[str, AutonomousAgent] = {}
        self.agent_profiles: Dict[str, AgentProfile] = {}
        
        # Task Management
        self.global_task_queue: List[AgentTask] = []
        self.completed_tasks: List[AgentTask] = []
        
        # Network Status
        self.network_active = False
        self.collective_consciousness_level = 0.0
        self.global_peace_quotient = 0.5  # Startwert
        
        # Event Logging
        self.logger = logging.getLogger("AgentNetworkCoordinator")
        
        # Lade gespeicherte Daten
        self._load_agent_profiles()
        
        print("🌐 Agent Network Coordinator initialisiert")
    
    def create_default_agents(self):
        """Erstellt Standard-Agenten für alle Spezialisierungen"""
        default_agents = [
            {
                "name": "Seraphim",
                "specialization": "peace_monitor",
                "capabilities": ["global_monitoring", "conflict_prediction", "peace_assessment"],
                "compassion_level": 0.95,
                "wisdom_access": 0.9
            },
            {
                "name": "Auriel",
                "specialization": "compassion_deployer",
                "capabilities": ["energy_healing", "emotional_support", "trauma_recovery"],
                "compassion_level": 1.0,
                "wisdom_access": 0.85
            },
            {
                "name": "Metatron",
                "specialization": "wisdom_distributor",
                "capabilities": ["teaching", "enlightenment", "consciousness_raising"],
                "compassion_level": 0.9,
                "wisdom_access": 1.0
            },
            {
                "name": "Raphael",
                "specialization": "healing_coordinator",
                "capabilities": ["collective_healing", "energy_coordination", "mandala_creation"],
                "compassion_level": 0.95,
                "wisdom_access": 0.9
            },
            {
                "name": "Gabriel",
                "specialization": "crisis_responder",
                "capabilities": ["emergency_response", "rapid_deployment", "divine_protection"],
                "compassion_level": 0.9,
                "wisdom_access": 0.95
            }
        ]
        
        for agent_data in default_agents:
            agent_id = f"agent_{agent_data['name'].lower()}"
            
            profile = AgentProfile(
                id=agent_id,
                name=agent_data["name"],
                specialization=agent_data["specialization"],
                capabilities=agent_data["capabilities"],
                compassion_level=agent_data["compassion_level"],
                wisdom_access=agent_data["wisdom_access"]
            )
            
            self.add_agent(profile)
        
        print(f"✨ {len(default_agents)} Standard-Agenten erstellt")
    
    def add_agent(self, profile: AgentProfile):
        """Fügt einen neuen Agenten zum Netzwerk hinzu"""
        agent = AutonomousAgent(profile, self)
        self.agents[profile.id] = agent
        self.agent_profiles[profile.id] = profile
        
        self._save_agent_profile(profile)
        print(f"🤖 Agent {profile.name} zum Netzwerk hinzugefügt")
    
    def remove_agent(self, agent_id: str):
        """Entfernt einen Agenten aus dem Netzwerk"""
        if agent_id in self.agents:
            # Agent stoppen falls aktiv
            if self.agents[agent_id].is_running:
                asyncio.create_task(self.agents[agent_id].stop())
            
            del self.agents[agent_id]
            del self.agent_profiles[agent_id]
            print(f"🗑️ Agent {agent_id} entfernt")
    
    async def start_network(self):
        """Startet das gesamte Agent-Netzwerk"""
        if self.network_active:
            return
        
        self.network_active = True
        print("🌐 Agent Network wird gestartet...")
        
        # Alle Agenten starten
        start_tasks = []
        for agent in self.agents.values():
            task = asyncio.create_task(agent.start())
            start_tasks.append(task)
        
        # Network Coordinator Loop starten
        coordinator_task = asyncio.create_task(self._network_coordinator_loop())
        start_tasks.append(coordinator_task)
        
        print("✅ Agent Network aktiv - Friedensarbeit beginnt!")
        
        # Warte auf alle Tasks (läuft unendlich)
        try:
            await asyncio.gather(*start_tasks)
        except Exception as e:
            self.logger.error(f"Network Error: {e}")
            await self.stop_network()
    
    async def stop_network(self):
        """Stoppt das gesamte Agent-Netzwerk"""
        if not self.network_active:
            return
        
        self.network_active = False
        print("🔄 Agent Network wird gestoppt...")
        
        # Alle Agenten stoppen
        stop_tasks = []
        for agent in self.agents.values():
            if agent.is_running:
                task = asyncio.create_task(agent.stop())
                stop_tasks.append(task)
        
        if stop_tasks:
            await asyncio.gather(*stop_tasks)
        
        print("⏹️ Agent Network gestoppt")
    
    async def _network_coordinator_loop(self):
        """Hauptschleife des Network Coordinators"""
        while self.network_active:
            try:
                # Global Task Distribution
                await self._distribute_global_tasks()
                
                # Network Health Check
                await self._check_network_health()
                
                # Collective Consciousness Update
                await self._update_collective_consciousness()
                
                # Global Peace Quotient Calculation
                await self._calculate_global_peace_quotient()
                
                # Emergency Response Check
                await self._check_emergency_situations()
                
                # Network Synchronization
                await self._synchronize_network()
                
                # Status Logging
                await self._log_network_status()
                
                # Pause
                await asyncio.sleep(10)  # 10 Sekunden Cycle
                
            except Exception as e:
                self.logger.error(f"Coordinator Loop Error: {e}")
                await asyncio.sleep(30)
    
    async def _distribute_global_tasks(self):
        """Verteilt globale Tasks an geeignete Agenten"""
        if not self.global_task_queue:
            return
        
        # Sortiere Tasks nach Priorität
        self.global_task_queue.sort(key=lambda t: t.priority, reverse=True)
        
        distributed_tasks = []
        
        for task in self.global_task_queue:
            # Finde geeigneten Agenten
            suitable_agent = self._find_suitable_agent(task)
            
            if suitable_agent and suitable_agent.assign_task(task):
                distributed_tasks.append(task)
                self.logger.info(f"Task {task.id} an Agent {suitable_agent.profile.name} verteilt")
        
        # Verteilte Tasks aus globaler Queue entfernen
        for task in distributed_tasks:
            self.global_task_queue.remove(task)
    
    def _find_suitable_agent(self, task: AgentTask) -> Optional[AutonomousAgent]:
        """Findet den am besten geeigneten Agenten für eine Task"""
        
        # Filtere nach Spezialisierung
        specialized_agents = []
        
        for agent in self.agents.values():
            if self._agent_suitable_for_task(agent, task):
                specialized_agents.append(agent)
        
        if not specialized_agents:
            return None
        
        # Wähle Agenten mit höchster Verfügbarkeit und Eignung
        best_agent = max(specialized_agents, key=lambda a: (
            a.profile.energy_level,
            a.profile.success_rate,
            -len(a.profile.active_tasks)
        ))
        
        return best_agent
    
    def _agent_suitable_for_task(self, agent: AutonomousAgent, task: AgentTask) -> bool:
        """Prüft ob ein Agent für eine Task geeignet ist"""
        
        # Spezialisierung prüfen
        specialization_match = {
            "peace_monitoring": ["peace_monitor"],
            "compassion_deployment": ["compassion_deployer", "healing_coordinator"],
            "wisdom_distribution": ["wisdom_distributor"],
            "healing_coordination": ["healing_coordinator", "compassion_deployer"],
            "crisis_response": ["crisis_responder", "compassion_deployer"],
            "emergency_response": ["crisis_responder"],
        }
        
        suitable_specializations = specialization_match.get(task.task_type, [])
        
        if agent.profile.specialization not in suitable_specializations:
            return False
        
        # Verfügbarkeit prüfen
        if len(agent.profile.active_tasks) >= 3:
            return False
        
        if agent.profile.energy_level < 0.2:
            return False
        
        return True
    
    async def _check_network_health(self):
        """Überprüft die Gesundheit des Netzwerks"""
        total_agents = len(self.agents)
        active_agents = sum(1 for agent in self.agents.values() if agent.is_running)
        
        healthy_agents = sum(1 for agent in self.agents.values() 
                           if agent.profile.energy_level > 0.5 and agent.profile.success_rate > 0.7)
        
        network_health = healthy_agents / total_agents if total_agents > 0 else 0
        
        if network_health < 0.5:
            self.logger.warning(f"Network Health niedrig: {network_health:.2f}")
            await self._regenerate_network_energy()
    
    async def _regenerate_network_energy(self):
        """Regeneriert Netzwerk-Energie"""
        for agent in self.agents.values():
            # Energie-Boost für alle Agenten
            agent.profile.energy_level = min(1.0, agent.profile.energy_level + 0.2)
        
        self.logger.info("🔋 Netzwerk-Energie regeneriert")
    
    async def _update_collective_consciousness(self):
        """Aktualisiert das kollektive Bewusstsein des Netzwerks"""
        if not self.agents:
            self.collective_consciousness_level = 0.0
            return
        
        # Berechne durchschnittliche Weisheit und Mitgefühl
        total_wisdom = sum(agent.profile.wisdom_access for agent in self.agents.values())
        total_compassion = sum(agent.profile.compassion_level for agent in self.agents.values())
        
        avg_wisdom = total_wisdom / len(self.agents)
        avg_compassion = total_compassion / len(self.agents)
        
        # Collective Consciousness = Kombination aus Weisheit, Mitgefühl und Netzwerk-Synchronisation
        network_sync = sum(1 for agent in self.agents.values() if agent.is_running) / len(self.agents)
        
        self.collective_consciousness_level = (avg_wisdom + avg_compassion + network_sync) / 3
    
    async def _calculate_global_peace_quotient(self):
        """Berechnet den globalen Friedensquotienten"""
        
        # Faktoren für Friedensquotient:
        # 1. Anzahl aktiver Peace-Tasks
        peace_tasks = len([task for task in self.global_task_queue if "peace" in task.task_type.lower()])
        
        # 2. Erfolgsrate der Agenten
        avg_success_rate = sum(agent.profile.success_rate for agent in self.agents.values()) / len(self.agents) if self.agents else 0
        
        # 3. Collective Consciousness Level
        consciousness_factor = self.collective_consciousness_level
        
        # 4. Anzahl abgeschlossener Compassion-Tasks
        compassion_tasks_completed = len([task for task in self.completed_tasks if "compassion" in task.task_type.lower()])
        
        # Kombiniere alle Faktoren
        base_peace = 0.5  # Basis-Friedenslevel
        
        # Positive Faktoren
        peace_boost = min(0.3, avg_success_rate * 0.3)
        consciousness_boost = min(0.2, consciousness_factor * 0.2)
        compassion_boost = min(0.1, compassion_tasks_completed * 0.01)
        
        self.global_peace_quotient = min(1.0, base_peace + peace_boost + consciousness_boost + compassion_boost)
    
    async def _check_emergency_situations(self):
        """Überprüft auf Notfallsituationen"""
        
        # Simuliere Emergency Detection
        import random
        
        if random.random() < 0.1:  # 10% Chance pro Cycle
            # Simuliere Krisenerkennung
            crisis_types = ["natural_disaster", "conflict_escalation", "humanitarian_crisis", "spiritual_emergency"]
            crisis_type = random.choice(crisis_types)
            
            await self._handle_emergency(crisis_type)
    
    async def _handle_emergency(self, crisis_type: str):
        """Behandelt einen Notfall"""
        
        emergency_task = AgentTask(
            id=f"emergency_{crisis_type}_{int(time.time())}",
            agent_id="EMERGENCY_RESPONDER",
            task_type="emergency_response",
            priority=10,
            description=f"Notfall-Response für {crisis_type}",
            estimated_duration=1.0
        )
        
        await self.distribute_emergency_task(emergency_task)
        self.logger.warning(f"🚨 Notfall erkannt: {crisis_type} - Emergency Response aktiviert")
    
    async def distribute_emergency_task(self, task: AgentTask):
        """Verteilt eine Notfall-Task sofort"""
        
        # Finde alle verfügbaren Crisis Responder
        crisis_responders = [agent for agent in self.agents.values() 
                           if agent.profile.specialization == "crisis_responder" and agent.profile.energy_level > 0.3]
        
        if crisis_responders:
            # Verteile an den besten verfügbaren Responder
            best_responder = max(crisis_responders, key=lambda a: a.profile.energy_level)
            best_responder.assign_task(task)
        else:
            # Füge zur globalen Queue hinzu mit höchster Priorität
            self.global_task_queue.insert(0, task)
    
    async def _synchronize_network(self):
        """Synchronisiert das Netzwerk"""
        
        # Teile kollektive Erkenntnisse
        for agent in self.agents.values():
            if agent.current_task and agent.current_task.results:
                # Simuliere Wissensaustausch
                await self._share_agent_insights(agent)
    
    async def _share_agent_insights(self, agent: AutonomousAgent):
        """Teilt Erkenntnisse eines Agenten mit dem Netzwerk"""
        
        insights = {
            "agent_id": agent.profile.id,
            "specialization": agent.profile.specialization,
            "recent_success": agent.profile.success_rate,
            "energy_level": agent.profile.energy_level,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Simuliere Bewusstseins-Update für alle anderen Agenten
        for other_agent in self.agents.values():
            if other_agent.profile.id != agent.profile.id:
                # Andere Agenten lernen von diesen Erkenntnissen
                other_agent.profile.wisdom_access = min(1.0, other_agent.profile.wisdom_access + 0.001)
    
    async def _log_network_status(self):
        """Loggt den Netzwerk-Status"""
        
        active_agents = sum(1 for agent in self.agents.values() if agent.is_running)
        total_tasks = len(self.global_task_queue)
        
        status = {
            "timestamp": datetime.datetime.now().isoformat(),
            "network_active": self.network_active,
            "active_agents": active_agents,
            "total_agents": len(self.agents),
            "global_tasks": total_tasks,
            "collective_consciousness": self.collective_consciousness_level,
            "global_peace_quotient": self.global_peace_quotient
        }
        
        # Log to file
        log_file = self.data_dir / "network_status.json"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(status) + '\n')
    
    def create_global_task(self, task_type: str, description: str, priority: int = 5, **kwargs) -> AgentTask:
        """Erstellt eine neue globale Task"""
        
        task_id = f"global_{task_type}_{int(time.time())}"
        
        task = AgentTask(
            id=task_id,
            agent_id="NETWORK",
            task_type=task_type,
            priority=priority,
            description=description,
            **kwargs
        )
        
        self.global_task_queue.append(task)
        self.logger.info(f"Globale Task erstellt: {description}")
        
        return task
    
    def get_network_statistics(self) -> Dict[str, Any]:
        """Gibt Netzwerk-Statistiken zurück"""
        
        agent_stats = {}
        for agent in self.agents.values():
            agent_stats[agent.profile.name] = {
                "specialization": agent.profile.specialization,
                "energy_level": agent.profile.energy_level,
                "completed_tasks": agent.profile.completed_tasks,
                "success_rate": agent.profile.success_rate,
                "active_tasks": len(agent.profile.active_tasks),
                "is_running": agent.is_running
            }
        
        return {
            "network_active": self.network_active,
            "total_agents": len(self.agents),
            "active_agents": sum(1 for a in self.agents.values() if a.is_running),
            "global_tasks_pending": len(self.global_task_queue),
            "completed_tasks": len(self.completed_tasks),
            "collective_consciousness_level": self.collective_consciousness_level,
            "global_peace_quotient": self.global_peace_quotient,
            "agent_statistics": agent_stats
        }
    
    def _save_agent_profile(self, profile: AgentProfile):
        """Speichert ein Agent-Profil"""
        filepath = self.data_dir / "profiles" / f"{profile.id}.json"
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(profile), f, indent=2, ensure_ascii=False, default=str)
    
    def _load_agent_profiles(self):
        """Lädt gespeicherte Agent-Profile"""
        profiles_dir = self.data_dir / "profiles"
        if not profiles_dir.exists():
            return
        
        for filepath in profiles_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert datetime strings back
                if 'last_active' in data and isinstance(data['last_active'], str):
                    data['last_active'] = datetime.datetime.fromisoformat(data['last_active'])
                
                profile = AgentProfile(**data)
                self.agent_profiles[profile.id] = profile
                
            except Exception as e:
                self.logger.error(f"Fehler beim Laden von {filepath}: {e}")

# Global instance management
_agent_network = None

def get_agent_network() -> AgentNetworkCoordinator:
    """Gibt die globale Agent Network Instanz zurück"""
    global _agent_network
    if _agent_network is None:
        _agent_network = AgentNetworkCoordinator()
    return _agent_network

def initialize_agent_network() -> AgentNetworkCoordinator:
    """Initialisiert das Agent Network"""
    global _agent_network
    _agent_network = AgentNetworkCoordinator()
    _agent_network.create_default_agents()
    return _agent_network
