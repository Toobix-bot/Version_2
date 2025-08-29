"""
🎨 ARTEFAKT SYSTEM ENGINE
========================

Kristallisiert Weisheit in visuelle Artefakte:
- AI-generierte Bilder für spirituelle Einsichten
- Wisdom Collections (Sammlungen von Erkenntnissen)
- Sacred Geometries & Mandalas
- Inspirational Quote Cards
- Personal Growth Visualizations
- Energy Healing Patterns
"""

import os
import json
import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
import hashlib
import base64
from pathlib import Path

@dataclass
class WisdomArtefakt:
    """Ein spirituelles Weisheits-Artefakt"""
    id: str
    title: str
    category: str  # "quote", "mandala", "visualization", "sacred_geometry", "healing"
    wisdom_text: str
    image_prompt: str
    image_path: Optional[str] = None
    metadata: Dict[str, Any] = None
    created_at: datetime.datetime = None
    spiritual_energy: float = 0.0  # 0-1 spirituelle Energie-Level
    manifestation_power: float = 0.0  # 0-1 Manifestations-Kraft
    healing_frequency: float = 0.0  # 0-1 Heilungs-Frequenz
    tags: List[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.now()
        if self.metadata is None:
            self.metadata = {}
        if self.tags is None:
            self.tags = []

@dataclass
class WisdomCollection:
    """Sammlung von Weisheits-Artefakten"""
    id: str
    name: str
    description: str
    artefakts: List[str]  # IDs der Artefakte
    theme: str  # "healing", "manifestation", "peace", "love", "wisdom"
    created_at: datetime.datetime = None
    energy_signature: Dict[str, float] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.now()
        if self.energy_signature is None:
            self.energy_signature = {}

class ArtefaktSystem:
    """
    🎨 ARTEFAKT CREATION ENGINE
    
    Kristallisiert spirituelle Weisheit in visuelle Form:
    - Generiert AI-Bilder für Einsichten
    - Erstellt Sacred Geometry Patterns
    - Sammelt Wisdom Collections
    - Manifestiert Healing Visuals
    """
    
    def __init__(self, ai_handler=None, data_dir="artefakt_data"):
        self.ai_handler = ai_handler
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Artefakt Storage
        self.artefakts: Dict[str, WisdomArtefakt] = {}
        self.collections: Dict[str, WisdomCollection] = {}
        
        # Image Generation
        self.image_generator = None
        self._initialize_image_generator()
        
        # Sacred Patterns Library
        self.sacred_patterns = self._load_sacred_patterns()
        
        # Load existing data
        self._load_artefakts()
        self._load_collections()
        
        print("🎨 Artefakt System initialisiert")
    
    def _initialize_image_generator(self):
        """Initialisiert Image Generation System"""
        try:
            # Try to initialize various image generation APIs
            # For now, we'll prepare the infrastructure
            self.image_generation_available = False
            
            # Check for environment variables for image APIs
            if os.getenv("OPENAI_API_KEY"):
                self.image_generation_available = True
                self.image_provider = "openai"
            elif os.getenv("STABILITY_API_KEY"):
                self.image_generation_available = True
                self.image_provider = "stability"
            else:
                print("⚠️ Keine Image Generation API verfügbar - verwende Placeholder System")
                self.image_provider = "placeholder"
            
        except Exception as e:
            print(f"⚠️ Image Generator Init Warning: {e}")
            self.image_generation_available = False
    
    def _load_sacred_patterns(self) -> Dict[str, Any]:
        """Lädt Sacred Geometry Patterns"""
        return {
            "flower_of_life": {
                "description": "Heilige Geometrie der Schöpfung",
                "energy": "manifestation",
                "prompt": "Sacred geometry flower of life pattern, golden ratio, spiritual energy, glowing sacred geometry, cosmic harmony, divine proportion"
            },
            "merkaba": {
                "description": "Lichtkörper-Aktivierung",
                "energy": "ascension",
                "prompt": "Merkaba light body activation, sacred geometry star tetrahedron, spinning energy field, spiritual ascension, light vehicle"
            },
            "sri_yantra": {
                "description": "Manifestations-Mandala",
                "energy": "abundance",
                "prompt": "Sri Yantra sacred geometry, cosmic manifestation mandala, golden triangles, divine feminine energy, abundance meditation"
            },
            "tree_of_life": {
                "description": "Kabbalistische Lebensbaum",
                "energy": "wisdom",
                "prompt": "Tree of life kabbalah, sacred pathways, divine wisdom, spiritual evolution, cosmic tree, sephiroth energy centers"
            },
            "chakra_mandala": {
                "description": "Energie-Zentren Heilung",
                "energy": "healing",
                "prompt": "Chakra healing mandala, seven energy centers, rainbow colors, spiritual healing, energy alignment, kundalini activation"
            }
        }
    
    def create_wisdom_artefakt(
        self,
        wisdom_text: str,
        category: str = "quote",
        title: Optional[str] = None,
        custom_prompt: Optional[str] = None,
        spiritual_theme: str = "general"
    ) -> WisdomArtefakt:
        """Erstellt ein neues Weisheits-Artefakt"""
        
        # Generate unique ID
        text_hash = hashlib.md5(wisdom_text.encode()).hexdigest()[:8]
        artefakt_id = f"{category}_{text_hash}_{int(datetime.datetime.now().timestamp())}"
        
        # Auto-generate title if not provided
        if not title:
            title = self._generate_title(wisdom_text, category)
        
        # Generate image prompt
        image_prompt = custom_prompt or self._generate_image_prompt(wisdom_text, category, spiritual_theme)
        
        # Calculate spiritual energies
        energies = self._calculate_spiritual_energies(wisdom_text, category)
        
        # Extract tags
        tags = self._extract_wisdom_tags(wisdom_text, category)
        
        # Create artefakt
        artefakt = WisdomArtefakt(
            id=artefakt_id,
            title=title,
            category=category,
            wisdom_text=wisdom_text,
            image_prompt=image_prompt,
            spiritual_energy=energies["spiritual"],
            manifestation_power=energies["manifestation"],
            healing_frequency=energies["healing"],
            tags=tags,
            metadata={
                "spiritual_theme": spiritual_theme,
                "generation_method": "ai_assisted",
                "energy_analysis": energies
            }
        )
        
        # Store artefakt
        self.artefakts[artefakt_id] = artefakt
        self._save_artefakt(artefakt)
        
        # Generate image (if available)
        if self.image_generation_available:
            self._generate_artefakt_image(artefakt)
        
        print(f"🎨 Weisheits-Artefakt erstellt: {title}")
        return artefakt
    
    def _generate_title(self, wisdom_text: str, category: str) -> str:
        """Generiert einen Titel für das Artefakt"""
        
        # Extract key concepts from wisdom text
        key_words = wisdom_text.split()[:10]  # First 10 words
        
        title_templates = {
            "quote": [
                "Weisheit des Herzens",
                "Spirituelle Erkenntnis",
                "Göttliche Einsicht",
                "Seelen-Wahrheit",
                "Licht der Erkenntnis"
            ],
            "mandala": [
                "Heilungs-Mandala",
                "Kosmisches Rad",
                "Spirituelles Zentrum",
                "Energie-Portal",
                "Heilige Geometrie"
            ],
            "visualization": [
                "Manifestations-Vision",
                "Spirituelle Schau",
                "Inneres Bild",
                "Seelen-Vision",
                "Göttliche Visualisierung"
            ],
            "sacred_geometry": [
                "Heilige Proportion",
                "Kosmische Geometrie",
                "Göttliches Muster",
                "Universelles Design",
                "Spirituelle Form"
            ],
            "healing": [
                "Heilungs-Energie",
                "Spirituelle Medizin",
                "Göttliche Heilung",
                "Energie-Transmission",
                "Heiliges Licht"
            ]
        }
        
        templates = title_templates.get(category, title_templates["quote"])
        
        # Use AI to generate if available
        if self.ai_handler:
            try:
                title_prompt = f"Erstelle einen spirituellen, poetischen Titel für diese Weisheit: '{wisdom_text[:100]}...' Kategorie: {category}. Nur der Titel, maximal 4 Worte:"
                title = self.ai_handler.get_response(title_prompt)
                if title and len(title.strip()) < 50:
                    return title.strip().strip('"').strip("'")
            except:
                pass
        
        # Fallback to template
        import random
        return random.choice(templates)
    
    def _generate_image_prompt(self, wisdom_text: str, category: str, theme: str) -> str:
        """Generiert einen Prompt für die Bildgenerierung"""
        
        base_prompts = {
            "quote": "Beautiful spiritual quote card design, elegant typography, peaceful background, soft colors, inspirational art, sacred symbols, divine light",
            "mandala": "Intricate mandala design, sacred geometry, spiritual patterns, cosmic harmony, healing colors, divine symmetry, meditation art",
            "visualization": "Spiritual visualization art, ethereal landscapes, divine light, cosmic energy, spiritual journey, transcendent imagery",
            "sacred_geometry": "Sacred geometry patterns, golden ratio, divine proportion, cosmic harmony, spiritual mathematics, universal design",
            "healing": "Healing energy visualization, chakra colors, spiritual light, energy flow, divine healing, therapeutic art, rainbow light"
        }
        
        # Theme enhancements
        theme_additions = {
            "peace": "peaceful energy, calm vibrations, serenity, tranquil atmosphere",
            "love": "heart energy, divine love, compassionate light, rose quartz colors",
            "wisdom": "ancient wisdom, spiritual knowledge, enlightenment, golden light",
            "healing": "healing energy, therapeutic colors, restorative light, wellness vibrations",
            "manifestation": "manifestation energy, creation power, abundance, golden abundance",
            "protection": "protective energy, spiritual shield, divine protection, sacred barrier"
        }
        
        base_prompt = base_prompts.get(category, base_prompts["quote"])
        theme_add = theme_additions.get(theme, "spiritual energy, divine light")
        
        # Extract keywords from wisdom text
        wisdom_keywords = self._extract_image_keywords(wisdom_text)
        
        # Combine prompts
        full_prompt = f"{base_prompt}, {theme_add}, {wisdom_keywords}, high quality, professional art, spiritual aesthetic, divine beauty"
        
        return full_prompt
    
    def _extract_image_keywords(self, text: str) -> str:
        """Extrahiert Schlüsselwörter für Bildgenerierung"""
        spiritual_keywords = {
            "light": "divine light, spiritual illumination",
            "peace": "peaceful energy, tranquility",
            "love": "heart energy, divine love",
            "healing": "healing light, therapeutic energy",
            "wisdom": "ancient wisdom, enlightenment",
            "strength": "inner strength, spiritual power",
            "journey": "spiritual path, sacred journey",
            "nature": "natural harmony, earth connection",
            "divine": "divine presence, sacred energy",
            "soul": "soul light, spiritual essence"
        }
        
        found_keywords = []
        text_lower = text.lower()
        
        for keyword, description in spiritual_keywords.items():
            if keyword in text_lower:
                found_keywords.append(description)
        
        return ", ".join(found_keywords[:3]) or "spiritual energy, divine harmony"
    
    def _calculate_spiritual_energies(self, text: str, category: str) -> Dict[str, float]:
        """Berechnet spirituelle Energie-Werte"""
        text_lower = text.lower()
        
        # Spiritual energy indicators
        spiritual_words = ["spirit", "divine", "sacred", "holy", "blessed", "enlighten", "transcend", "cosmic", "universal"]
        manifestation_words = ["manifest", "create", "abundance", "attract", "achieve", "success", "power", "strength"]
        healing_words = ["heal", "peace", "calm", "restore", "balance", "harmony", "wellness", "therapy"]
        
        spiritual_score = sum(1 for word in spiritual_words if word in text_lower) / len(spiritual_words)
        manifestation_score = sum(1 for word in manifestation_words if word in text_lower) / len(manifestation_words)
        healing_score = sum(1 for word in healing_words if word in text_lower) / len(healing_words)
        
        # Category bonuses
        category_bonuses = {
            "sacred_geometry": {"spiritual": 0.3, "manifestation": 0.2, "healing": 0.1},
            "mandala": {"spiritual": 0.2, "manifestation": 0.1, "healing": 0.3},
            "healing": {"spiritual": 0.1, "manifestation": 0.0, "healing": 0.4},
            "visualization": {"spiritual": 0.1, "manifestation": 0.3, "healing": 0.1},
            "quote": {"spiritual": 0.2, "manifestation": 0.1, "healing": 0.1}
        }
        
        bonuses = category_bonuses.get(category, {"spiritual": 0, "manifestation": 0, "healing": 0})
        
        return {
            "spiritual": min(1.0, spiritual_score + bonuses["spiritual"]),
            "manifestation": min(1.0, manifestation_score + bonuses["manifestation"]),
            "healing": min(1.0, healing_score + bonuses["healing"])
        }
    
    def _extract_wisdom_tags(self, text: str, category: str) -> List[str]:
        """Extrahiert Tags aus dem Weisheits-Text"""
        text_lower = text.lower()
        
        tag_keywords = {
            "love": ["love", "heart", "compassion", "kindness"],
            "peace": ["peace", "calm", "serenity", "tranquil"],
            "wisdom": ["wisdom", "knowledge", "understanding", "insight"],
            "healing": ["heal", "restore", "balance", "wellness"],
            "strength": ["strength", "power", "courage", "brave"],
            "gratitude": ["grateful", "thankful", "blessing", "appreciate"],
            "forgiveness": ["forgive", "mercy", "release", "let go"],
            "manifestation": ["manifest", "create", "attract", "abundance"],
            "spiritual": ["spirit", "soul", "divine", "sacred"],
            "growth": ["grow", "evolve", "transform", "change"]
        }
        
        found_tags = [category]  # Always include category
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                found_tags.append(tag)
        
        # Remove duplicates and limit
        return list(set(found_tags))[:5]
    
    def _generate_artefakt_image(self, artefakt: WisdomArtefakt):
        """Generiert das Bild für ein Artefakt"""
        try:
            if self.image_provider == "placeholder":
                # Create placeholder image info
                artefakt.image_path = f"placeholder_{artefakt.id}.jpg"
                artefakt.metadata["image_status"] = "placeholder"
                print(f"📸 Placeholder Image für {artefakt.title}")
                return
            
            # Here would be actual image generation
            # For now, we simulate the process
            image_filename = f"{artefakt.id}.jpg"
            image_path = self.data_dir / "images" / image_filename
            image_path.parent.mkdir(exist_ok=True)
            
            # Simulate image generation delay
            print(f"🎨 Generiere Bild für: {artefakt.title}")
            
            # In a real implementation, this would call:
            # - OpenAI DALL-E API
            # - Stability AI API
            # - Local Stable Diffusion
            # etc.
            
            artefakt.image_path = str(image_path)
            artefakt.metadata["image_status"] = "generated"
            artefakt.metadata["image_prompt"] = artefakt.image_prompt
            
        except Exception as e:
            print(f"⚠️ Image Generation Error: {e}")
            artefakt.metadata["image_status"] = "failed"
    
    def create_sacred_geometry_artefakt(self, pattern_name: str, intention: str = "") -> WisdomArtefakt:
        """Erstellt ein Sacred Geometry Artefakt"""
        
        if pattern_name not in self.sacred_patterns:
            raise ValueError(f"Pattern '{pattern_name}' nicht verfügbar")
        
        pattern = self.sacred_patterns[pattern_name]
        
        wisdom_text = f"Heilige Geometrie: {pattern['description']}. {intention}".strip()
        
        return self.create_wisdom_artefakt(
            wisdom_text=wisdom_text,
            category="sacred_geometry",
            title=f"{pattern_name.replace('_', ' ').title()} - {pattern['description']}",
            custom_prompt=pattern["prompt"],
            spiritual_theme=pattern["energy"]
        )
    
    def create_healing_artefakt(self, healing_intention: str, target_area: str = "general") -> WisdomArtefakt:
        """Erstellt ein Heilungs-Artefakt"""
        
        healing_prompts = {
            "general": "Universal healing energy, rainbow light, chakra alignment, divine healing",
            "emotional": "Heart healing, emotional balance, rose quartz energy, compassionate light",
            "physical": "Physical healing energy, green healing light, cellular regeneration, vitality",
            "mental": "Mental clarity, peaceful mind, blue healing light, cognitive harmony",
            "spiritual": "Spiritual healing, divine connection, violet flame, soul restoration"
        }
        
        base_prompt = healing_prompts.get(target_area, healing_prompts["general"])
        
        wisdom_text = f"Heilungs-Intention: {healing_intention}. Zielbereich: {target_area}"
        
        return self.create_wisdom_artefakt(
            wisdom_text=wisdom_text,
            category="healing",
            title=f"Heilung für {target_area}: {healing_intention}",
            custom_prompt=f"{base_prompt}, {healing_intention}, therapeutic art, healing visualization",
            spiritual_theme="healing"
        )
    
    def create_collection(
        self,
        name: str,
        description: str,
        theme: str,
        artefakt_ids: List[str] = None
    ) -> WisdomCollection:
        """Erstellt eine neue Wisdom Collection"""
        
        collection_id = f"collection_{hashlib.md5(name.encode()).hexdigest()[:8]}_{int(datetime.datetime.now().timestamp())}"
        
        collection = WisdomCollection(
            id=collection_id,
            name=name,
            description=description,
            theme=theme,
            artefakts=artefakt_ids or []
        )
        
        # Calculate energy signature
        if collection.artefakts:
            collection.energy_signature = self._calculate_collection_energy(collection.artefakts)
        
        self.collections[collection_id] = collection
        self._save_collection(collection)
        
        print(f"📚 Wisdom Collection erstellt: {name}")
        return collection
    
    def add_to_collection(self, collection_id: str, artefakt_id: str):
        """Fügt ein Artefakt zu einer Collection hinzu"""
        if collection_id in self.collections and artefakt_id in self.artefakts:
            if artefakt_id not in self.collections[collection_id].artefakts:
                self.collections[collection_id].artefakts.append(artefakt_id)
                
                # Update energy signature
                self.collections[collection_id].energy_signature = self._calculate_collection_energy(
                    self.collections[collection_id].artefakts
                )
                
                self._save_collection(self.collections[collection_id])
                print(f"✅ Artefakt zu Collection '{self.collections[collection_id].name}' hinzugefügt")
    
    def _calculate_collection_energy(self, artefakt_ids: List[str]) -> Dict[str, float]:
        """Berechnet die Energie-Signatur einer Collection"""
        if not artefakt_ids:
            return {"spiritual": 0.0, "manifestation": 0.0, "healing": 0.0}
        
        total_spiritual = 0.0
        total_manifestation = 0.0
        total_healing = 0.0
        
        valid_artefakts = 0
        
        for artefakt_id in artefakt_ids:
            if artefakt_id in self.artefakts:
                artefakt = self.artefakts[artefakt_id]
                total_spiritual += artefakt.spiritual_energy
                total_manifestation += artefakt.manifestation_power
                total_healing += artefakt.healing_frequency
                valid_artefakts += 1
        
        if valid_artefakts == 0:
            return {"spiritual": 0.0, "manifestation": 0.0, "healing": 0.0}
        
        return {
            "spiritual": total_spiritual / valid_artefakts,
            "manifestation": total_manifestation / valid_artefakts,
            "healing": total_healing / valid_artefakts
        }
    
    def get_artefakts_by_theme(self, theme: str) -> List[WisdomArtefakt]:
        """Filtert Artefakte nach spirituellem Thema"""
        filtered = []
        
        for artefakt in self.artefakts.values():
            if (theme in artefakt.tags or 
                artefakt.metadata.get("spiritual_theme") == theme or
                theme.lower() in artefakt.wisdom_text.lower()):
                filtered.append(artefakt)
        
        # Sort by spiritual energy
        return sorted(filtered, key=lambda a: a.spiritual_energy, reverse=True)
    
    def get_high_energy_artefakts(self, energy_type: str = "spiritual", min_threshold: float = 0.7) -> List[WisdomArtefakt]:
        """Gibt hochenergetische Artefakte zurück"""
        energy_attr = {
            "spiritual": "spiritual_energy",
            "manifestation": "manifestation_power",
            "healing": "healing_frequency"
        }.get(energy_type, "spiritual_energy")
        
        filtered = [
            artefakt for artefakt in self.artefakts.values()
            if getattr(artefakt, energy_attr) >= min_threshold
        ]
        
        return sorted(filtered, key=lambda a: getattr(a, energy_attr), reverse=True)
    
    def export_collection(self, collection_id: str, export_format: str = "json") -> str:
        """Exportiert eine Collection"""
        if collection_id not in self.collections:
            raise ValueError(f"Collection {collection_id} nicht gefunden")
        
        collection = self.collections[collection_id]
        
        export_data = {
            "collection": asdict(collection),
            "artefakts": [
                asdict(self.artefakts[aid]) for aid in collection.artefakts
                if aid in self.artefakts
            ],
            "export_timestamp": datetime.datetime.now().isoformat(),
            "export_format": export_format
        }
        
        if export_format == "json":
            filename = f"collection_{collection.name.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = self.data_dir / "exports" / filename
            filepath.parent.mkdir(exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
            
            return str(filepath)
    
    def _save_artefakt(self, artefakt: WisdomArtefakt):
        """Speichert ein Artefakt"""
        filepath = self.data_dir / "artefakts" / f"{artefakt.id}.json"
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(artefakt), f, indent=2, ensure_ascii=False, default=str)
    
    def _save_collection(self, collection: WisdomCollection):
        """Speichert eine Collection"""
        filepath = self.data_dir / "collections" / f"{collection.id}.json"
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(collection), f, indent=2, ensure_ascii=False, default=str)
    
    def _load_artefakts(self):
        """Lädt gespeicherte Artefakte"""
        artefakts_dir = self.data_dir / "artefakts"
        if not artefakts_dir.exists():
            return
        
        for filepath in artefakts_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert datetime strings back
                if 'created_at' in data and isinstance(data['created_at'], str):
                    data['created_at'] = datetime.datetime.fromisoformat(data['created_at'])
                
                artefakt = WisdomArtefakt(**data)
                self.artefakts[artefakt.id] = artefakt
                
            except Exception as e:
                print(f"⚠️ Fehler beim Laden von {filepath}: {e}")
    
    def _load_collections(self):
        """Lädt gespeicherte Collections"""
        collections_dir = self.data_dir / "collections"
        if not collections_dir.exists():
            return
        
        for filepath in collections_dir.glob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert datetime strings back
                if 'created_at' in data and isinstance(data['created_at'], str):
                    data['created_at'] = datetime.datetime.fromisoformat(data['created_at'])
                
                collection = WisdomCollection(**data)
                self.collections[collection.id] = collection
                
            except Exception as e:
                print(f"⚠️ Fehler beim Laden von {filepath}: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Gibt Statistiken über das Artefakt System zurück"""
        total_artefakts = len(self.artefakts)
        total_collections = len(self.collections)
        
        # Categorize artefakts
        categories = {}
        themes = {}
        avg_energies = {"spiritual": 0.0, "manifestation": 0.0, "healing": 0.0}
        
        if total_artefakts > 0:
            for artefakt in self.artefakts.values():
                # Categories
                categories[artefakt.category] = categories.get(artefakt.category, 0) + 1
                
                # Themes
                theme = artefakt.metadata.get("spiritual_theme", "general")
                themes[theme] = themes.get(theme, 0) + 1
                
                # Energies
                avg_energies["spiritual"] += artefakt.spiritual_energy
                avg_energies["manifestation"] += artefakt.manifestation_power
                avg_energies["healing"] += artefakt.healing_frequency
            
            # Calculate averages
            for key in avg_energies:
                avg_energies[key] /= total_artefakts
        
        return {
            "total_artefakts": total_artefakts,
            "total_collections": total_collections,
            "categories": categories,
            "themes": themes,
            "average_energies": avg_energies,
            "image_generation_available": self.image_generation_available,
            "sacred_patterns_count": len(self.sacred_patterns)
        }

# Global instance management
_artefakt_system = None

def get_artefakt_system(ai_handler=None) -> ArtefaktSystem:
    """Gibt die globale ArtefaktSystem Instanz zurück"""
    global _artefakt_system
    if _artefakt_system is None:
        _artefakt_system = ArtefaktSystem(ai_handler)
    return _artefakt_system

def initialize_artefakt_system(ai_handler=None) -> ArtefaktSystem:
    """Initialisiert das Artefakt System"""
    global _artefakt_system
    _artefakt_system = ArtefaktSystem(ai_handler)
    return _artefakt_system
