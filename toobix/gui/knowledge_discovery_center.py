"""
Knowledge Discovery Center GUI - Phase 5.2
Interaktive Benutzeroberfläche für die Wissensbasis
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Callable, Optional
import logging

try:
    import customtkinter as ctk
    CTK_AVAILABLE = True
except ImportError:
    CTK_AVAILABLE = False

from toobix.core.knowledge_discovery_engine import (
    KnowledgeDiscoveryEngine, 
    KnowledgeItem, 
    KnowledgeCategory,
    LearningPath
)

logger = logging.getLogger(__name__)

class KnowledgeDiscoveryCenter:
    """
    GUI für das Knowledge Discovery Center
    Ermöglicht interaktives Browsen und Erkunden der Wissensbasis
    """
    
    def __init__(self, parent, knowledge_engine: KnowledgeDiscoveryEngine, action_callback: Callable[[str], None]):
        self.parent = parent
        self.knowledge_engine = knowledge_engine
        self.action_callback = action_callback
        
        self.current_category = None
        self.current_item = None
        self.search_results = []
        
        self._create_center()
        logger.info("📚 Knowledge Discovery Center initialisiert")
    
    def _create_center(self):
        """Erstellt das Knowledge Discovery Center"""
        # Main window für Knowledge Center
        self.center_window = None
        
    def show_center(self):
        """Zeigt das Knowledge Discovery Center"""
        if self.center_window and self.center_window.winfo_exists():
            self.center_window.lift()
            return
        
        self.center_window = tk.Toplevel(self.parent)
        self.center_window.title("📚 Toobix Knowledge Discovery Center")
        self.center_window.geometry("1000x700")
        self.center_window.resizable(True, True)
        
        # Main layout
        self._create_layout()
        self._populate_categories()
    
    def _create_layout(self):
        """Erstellt das Hauptlayout"""
        # === HEADER ===
        header_frame = ttk.Frame(self.center_window)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="📚 Knowledge Discovery Center", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(side="left")
        
        # Search
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side="right")
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame, 
            textvariable=self.search_var,
            width=30,
            font=("Arial", 10)
        )
        search_entry.pack(side="left", padx=(0, 5))
        search_entry.bind("<Return>", self._on_search)
        
        search_btn = ttk.Button(
            search_frame,
            text="🔍",
            width=3,
            command=self._on_search
        )
        search_btn.pack(side="left")
        
        # === MAIN CONTENT ===
        main_frame = ttk.Frame(self.center_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Left Panel - Navigation
        self.left_panel = ttk.LabelFrame(main_frame, text="Navigation", padding=10)
        self.left_panel.pack(side="left", fill="y", padx=(0, 5))
        
        # Center Panel - Content
        self.center_panel = ttk.LabelFrame(main_frame, text="Inhalt", padding=10)
        self.center_panel.pack(side="left", fill="both", expand=True, padx=5)
        
        # Right Panel - Details
        self.right_panel = ttk.LabelFrame(main_frame, text="Details", padding=10)
        self.right_panel.pack(side="right", fill="y", padx=(5, 0))
        
        # === FOOTER ===
        footer_frame = ttk.Frame(self.center_window)
        footer_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.status_label = ttk.Label(footer_frame, text="Bereit zum Erkunden...")
        self.status_label.pack(side="left")
        
        close_btn = ttk.Button(footer_frame, text="Schließen", command=self.center_window.destroy)
        close_btn.pack(side="right")
        
        # Setup panels
        self._setup_navigation_panel()
        self._setup_content_panel()
        self._setup_details_panel()
    
    def _setup_navigation_panel(self):
        """Erstellt das Navigations-Panel"""
        # Categories Tree
        categories_label = ttk.Label(self.left_panel, text="📂 Kategorien", font=("Arial", 11, "bold"))
        categories_label.pack(anchor="w", pady=(0, 5))
        
        # Treeview für Kategorien
        self.categories_tree = ttk.Treeview(self.left_panel, height=8)
        self.categories_tree.pack(fill="both", expand=True, pady=(0, 10))
        self.categories_tree.bind("<<TreeviewSelect>>", self._on_category_select)
        
        # Learning Paths
        paths_label = ttk.Label(self.left_panel, text="🎓 Lernpfade", font=("Arial", 11, "bold"))
        paths_label.pack(anchor="w", pady=(10, 5))
        
        self.paths_listbox = tk.Listbox(self.left_panel, height=4)
        self.paths_listbox.pack(fill="x", pady=(0, 10))
        self.paths_listbox.bind("<<ListboxSelect>>", self._on_path_select)
        
        # Quick Actions
        actions_label = ttk.Label(self.left_panel, text="⚡ Quick Actions", font=("Arial", 11, "bold"))
        actions_label.pack(anchor="w", pady=(10, 5))
        
        ttk.Button(self.left_panel, text="🔥 Beliebte Features", command=self._show_popular).pack(fill="x", pady=2)
        ttk.Button(self.left_panel, text="🎯 Empfehlungen", command=self._show_recommendations).pack(fill="x", pady=2)
        ttk.Button(self.left_panel, text="📊 Statistiken", command=self._show_statistics).pack(fill="x", pady=2)
    
    def _setup_content_panel(self):
        """Erstellt das Content-Panel"""
        # Content display mit Scrollbar
        self.content_canvas = tk.Canvas(self.center_panel)
        content_scrollbar = ttk.Scrollbar(self.center_panel, orient="vertical", command=self.content_canvas.yview)
        self.content_frame = ttk.Frame(self.content_canvas)
        
        self.content_canvas.configure(yscrollcommand=content_scrollbar.set)
        self.content_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        self.content_canvas.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")
        
        # Update scroll region when content changes
        def _on_frame_configure(event):
            self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))
        self.content_frame.bind("<Configure>", _on_frame_configure)
        
        # Welcome message
        self._show_welcome()
    
    def _setup_details_panel(self):
        """Erstellt das Details-Panel"""
        # Item details
        self.details_text = tk.Text(
            self.right_panel,
            width=30,
            height=20,
            wrap="word",
            font=("Arial", 9)
        )
        details_scrollbar = ttk.Scrollbar(self.right_panel, orient="vertical", command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.pack(side="left", fill="both", expand=True)
        details_scrollbar.pack(side="right", fill="y")
        
        # Action buttons
        button_frame = ttk.Frame(self.right_panel)
        button_frame.pack(fill="x", pady=(10, 0))
        
        self.try_button = ttk.Button(button_frame, text="🚀 Ausprobieren", command=self._try_current_item)
        self.try_button.pack(fill="x", pady=2)
        
        self.rate_button = ttk.Button(button_frame, text="⭐ Bewerten", command=self._rate_current_item)
        self.rate_button.pack(fill="x", pady=2)
    
    def _populate_categories(self):
        """Füllt die Kategorien"""
        # Clear existing
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        # Add categories
        categories = self.knowledge_engine.get_all_categories()
        for category in categories:
            cat_node = self.categories_tree.insert(
                "",
                "end",
                text=f"{category.icon} {category.name}",
                values=[category.id]
            )
            
            # Add items as children
            for item in category.items:
                self.categories_tree.insert(
                    cat_node,
                    "end",
                    text=f"📄 {item.title}",
                    values=[item.id]
                )
        
        # Populate learning paths
        self.paths_listbox.delete(0, tk.END)
        paths = self.knowledge_engine.get_all_learning_paths()
        for path in paths:
            self.paths_listbox.insert(tk.END, f"🎓 {path.title}")
        
        self.status_label.config(text=f"{len(categories)} Kategorien, {len(self.knowledge_engine.knowledge_base)} Features verfügbar")
    
    def _show_welcome(self):
        """Zeigt Willkommensnachricht"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        welcome_label = ttk.Label(
            self.content_frame,
            text="🌟 Willkommen im Knowledge Discovery Center!",
            font=("Arial", 14, "bold")
        )
        welcome_label.pack(pady=20)
        
        description = ttk.Label(
            self.content_frame,
            text="""
Hier kannst du alle Toobix-Features erkunden und lernen:

📂 Navigiere durch die Kategorien links
🔍 Nutze die Suche um spezifische Features zu finden  
🎓 Folge den strukturierten Lernpfaden
⚡ Probiere Quick Actions für sofortige Einblicke

Klicke auf eine Kategorie oder ein Feature um zu starten!
            """,
            font=("Arial", 10),
            justify="left"
        )
        description.pack(pady=20, padx=20)
        
        # Quick stats
        stats_frame = ttk.LabelFrame(self.content_frame, text="📊 Übersicht", padding=10)
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        categories = self.knowledge_engine.get_all_categories()
        total_items = len(self.knowledge_engine.knowledge_base)
        paths = len(self.knowledge_engine.get_all_learning_paths())
        
        stats_text = f"""
🗂️ Kategorien: {len(categories)}
📄 Features: {total_items}  
🎓 Lernpfade: {paths}
⭐ Bewertungen: Verfügbar
        """.strip()
        
        stats_label = ttk.Label(stats_frame, text=stats_text, font=("Arial", 10))
        stats_label.pack()
    
    def _on_category_select(self, event):
        """Behandelt Kategorie-Auswahl"""
        selection = self.categories_tree.selection()
        if not selection:
            return
        
        item = self.categories_tree.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        item_id = values[0]
        
        # Check if it's a category or knowledge item
        category = self.knowledge_engine.get_category(item_id)
        if category:
            self._show_category(category)
        else:
            knowledge_item = self.knowledge_engine.get_item(item_id)
            if knowledge_item:
                self._show_item(knowledge_item)
    
    def _show_category(self, category: KnowledgeCategory):
        """Zeigt Kategorie-Übersicht"""
        self.current_category = category
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Category header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=10)
        
        title_label = ttk.Label(
            header_frame,
            text=f"{category.icon} {category.name}",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        desc_label = ttk.Label(
            header_frame,
            text=category.description,
            font=("Arial", 10),
            foreground="gray"
        )
        desc_label.pack(pady=(5, 0))
        
        # Items grid
        items_frame = ttk.LabelFrame(self.content_frame, text=f"Features ({len(category.items)})", padding=10)
        items_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create grid of items
        row = 0
        col = 0
        for item in category.items:
            item_frame = ttk.Frame(items_frame, relief="raised", borderwidth=1)
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            # Item button
            item_btn = ttk.Button(
                item_frame,
                text=f"📄 {item.title}",
                command=lambda i=item: self._show_item(i)
            )
            item_btn.pack(fill="x", padx=5, pady=5)
            
            # Difficulty and usage
            info_label = ttk.Label(
                item_frame,
                text=f"{item.difficulty_level.title()} | {item.usage_count} mal genutzt",
                font=("Arial", 8),
                foreground="gray"
            )
            info_label.pack(pady=(0, 5))
            
            col += 1
            if col >= 2:  # 2 columns
                col = 0
                row += 1
        
        # Configure grid weights
        for i in range(2):
            items_frame.grid_columnconfigure(i, weight=1)
        
        self.status_label.config(text=f"Kategorie: {category.name} - {len(category.items)} Features")
    
    def _show_item(self, item: KnowledgeItem):
        """Zeigt detaillierte Item-Informationen"""
        self.current_item = item
        
        # Track usage
        self.knowledge_engine.track_usage(item.id)
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Item header
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=10)
        
        title_label = ttk.Label(
            header_frame,
            text=f"📄 {item.title}",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        # Meta info
        meta_frame = ttk.Frame(header_frame)
        meta_frame.pack(fill="x", pady=5)
        
        ttk.Label(meta_frame, text=f"Kategorie: {item.category.title()}", font=("Arial", 9)).pack(side="left")
        ttk.Label(meta_frame, text=f"Level: {item.difficulty_level.title()}", font=("Arial", 9)).pack(side="left", padx=(20, 0))
        ttk.Label(meta_frame, text=f"Genutzt: {item.usage_count}x", font=("Arial", 9)).pack(side="left", padx=(20, 0))
        
        if item.user_rating > 0:
            ttk.Label(meta_frame, text=f"Bewertung: ⭐{item.user_rating:.1f}", font=("Arial", 9)).pack(side="left", padx=(20, 0))
        
        # Description
        desc_frame = ttk.LabelFrame(self.content_frame, text="Beschreibung", padding=10)
        desc_frame.pack(fill="x", padx=10, pady=5)
        
        desc_label = ttk.Label(desc_frame, text=item.description, font=("Arial", 10), wraplength=600)
        desc_label.pack()
        
        # Content
        content_frame = ttk.LabelFrame(self.content_frame, text="Details", padding=10)
        content_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        content_text = tk.Text(content_frame, wrap="word", height=15, font=("Arial", 9))
        content_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=content_text.yview)
        content_text.configure(yscrollcommand=content_scrollbar.set)
        
        content_text.pack(side="left", fill="both", expand=True)
        content_scrollbar.pack(side="right", fill="y")
        
        content_text.insert("1.0", item.content)
        content_text.configure(state="disabled")
        
        # Examples
        if item.examples:
            examples_frame = ttk.LabelFrame(self.content_frame, text="Beispiele", padding=10)
            examples_frame.pack(fill="x", padx=10, pady=5)
            
            for i, example in enumerate(item.examples):
                example_label = ttk.Label(examples_frame, text=f"• {example}", font=("Arial", 9), wraplength=600)
                example_label.pack(anchor="w", pady=2)
        
        # Tags
        if item.tags:
            tags_frame = ttk.Frame(self.content_frame)
            tags_frame.pack(fill="x", padx=10, pady=5)
            
            ttk.Label(tags_frame, text="Tags:", font=("Arial", 9, "bold")).pack(side="left")
            
            for tag in item.tags:
                tag_label = ttk.Label(
                    tags_frame,
                    text=f"#{tag}",
                    font=("Arial", 8),
                    foreground="blue"
                )
                tag_label.pack(side="left", padx=(5, 0))
        
        # Update details panel
        self._update_details_panel(item)
        
        self.status_label.config(text=f"Feature: {item.title} | {item.category.title()}")
    
    def _update_details_panel(self, item: KnowledgeItem):
        """Aktualisiert das Details-Panel"""
        # Details Text bearbeitbar machen
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", tk.END)
        
        details = f"""📄 {item.title}

📋 ÜBERSICHT:
{item.description}

🎯 SCHWIERIGKEIT:
{item.difficulty_level.title()}

📊 NUTZUNG:
{item.usage_count} mal verwendet

🏷️ TAGS:
{', '.join(item.tags)}

📅 LETZTE AKTUALISIERUNG:
{item.last_updated[:10]}
"""
        
        if item.user_rating > 0:
            details += f"\n⭐ BEWERTUNG:\n{item.user_rating:.1f}/5.0"
        
        if item.related_items:
            details += f"\n\n🔗 VERWANDTE FEATURES:\n"
            for related_id in item.related_items:
                related_item = self.knowledge_engine.get_item(related_id)
                if related_item:
                    details += f"• {related_item.title}\n"
        
        self.details_text.insert("1.0", details)
        # Wieder schreibgeschützt machen
        self.details_text.configure(state="disabled")
    
    def _on_search(self, event=None):
        """Behandelt Suche"""
        query = self.search_var.get().strip()
        if not query:
            return
        
        results = self.knowledge_engine.search(query)
        self._show_search_results(query, results)
    
    def _show_search_results(self, query: str, results: List[KnowledgeItem]):
        """Zeigt Suchergebnisse"""
        self.search_results = results
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Search header
        header_label = ttk.Label(
            self.content_frame,
            text=f"🔍 Suchergebnisse für '{query}'",
            font=("Arial", 14, "bold")
        )
        header_label.pack(pady=10)
        
        if not results:
            no_results_label = ttk.Label(
                self.content_frame,
                text="Keine Ergebnisse gefunden. Versuche andere Suchbegriffe.",
                font=("Arial", 10),
                foreground="gray"
            )
            no_results_label.pack(pady=20)
            return
        
        # Results
        results_frame = ttk.LabelFrame(self.content_frame, text=f"{len(results)} Ergebnisse", padding=10)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for item in results:
            result_frame = ttk.Frame(results_frame, relief="groove", borderwidth=1)
            result_frame.pack(fill="x", pady=5, padx=5)
            
            # Title button
            title_btn = ttk.Button(
                result_frame,
                text=f"📄 {item.title}",
                command=lambda i=item: self._show_item(i)
            )
            title_btn.pack(anchor="w", padx=5, pady=2)
            
            # Description
            desc_label = ttk.Label(
                result_frame,
                text=item.description,
                font=("Arial", 9),
                foreground="gray",
                wraplength=500
            )
            desc_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        self.status_label.config(text=f"Suche: {len(results)} Ergebnisse für '{query}'")
    
    def _on_path_select(self, event):
        """Behandelt Learning Path Auswahl"""
        selection = self.paths_listbox.curselection()
        if not selection:
            return
        
        paths = self.knowledge_engine.get_all_learning_paths()
        if selection[0] < len(paths):
            path = paths[selection[0]]
            self._show_learning_path(path)
    
    def _show_learning_path(self, path: LearningPath):
        """Zeigt Learning Path"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Path header
        header_label = ttk.Label(
            self.content_frame,
            text=f"🎓 {path.title}",
            font=("Arial", 16, "bold")
        )
        header_label.pack(pady=10)
        
        desc_label = ttk.Label(
            self.content_frame,
            text=path.description,
            font=("Arial", 10),
            wraplength=600
        )
        desc_label.pack(pady=5)
        
        # Path info
        info_frame = ttk.Frame(self.content_frame)
        info_frame.pack(pady=10)
        
        ttk.Label(info_frame, text=f"⏱️ Geschätzte Zeit: {path.estimated_time} Minuten", font=("Arial", 9)).pack(side="left")
        ttk.Label(info_frame, text=f"📋 Schritte: {len(path.steps)}", font=("Arial", 9)).pack(side="left", padx=(20, 0))
        
        # Steps
        steps_frame = ttk.LabelFrame(self.content_frame, text="Lernschritte", padding=10)
        steps_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for i, step_id in enumerate(path.steps):
            item = self.knowledge_engine.get_item(step_id)
            if item:
                step_frame = ttk.Frame(steps_frame, relief="raised", borderwidth=1)
                step_frame.pack(fill="x", pady=5)
                
                step_btn = ttk.Button(
                    step_frame,
                    text=f"{i+1}. {item.title}",
                    command=lambda it=item: self._show_item(it)
                )
                step_btn.pack(fill="x", padx=5, pady=5)
                
                ttk.Label(
                    step_frame,
                    text=item.description,
                    font=("Arial", 9),
                    foreground="gray",
                    wraplength=500
                ).pack(padx=20, pady=(0, 5))
        
        self.status_label.config(text=f"Lernpfad: {path.title} - {len(path.steps)} Schritte")
    
    def _show_popular(self):
        """Zeigt beliebte Features"""
        popular = self.knowledge_engine.get_popular_items()
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        header_label = ttk.Label(
            self.content_frame,
            text="🔥 Beliebte Features",
            font=("Arial", 16, "bold")
        )
        header_label.pack(pady=10)
        
        if not popular:
            ttk.Label(
                self.content_frame,
                text="Noch keine Nutzungsstatistiken verfügbar.",
                font=("Arial", 10),
                foreground="gray"
            ).pack(pady=20)
            return
        
        popular_frame = ttk.LabelFrame(self.content_frame, text="Top Features", padding=10)
        popular_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for i, item in enumerate(popular):
            item_frame = ttk.Frame(popular_frame, relief="groove", borderwidth=1)
            item_frame.pack(fill="x", pady=5)
            
            rank_label = ttk.Label(item_frame, text=f"#{i+1}", font=("Arial", 12, "bold"))
            rank_label.pack(side="left", padx=10, pady=10)
            
            content_frame = ttk.Frame(item_frame)
            content_frame.pack(side="left", fill="x", expand=True, padx=10, pady=5)
            
            title_btn = ttk.Button(
                content_frame,
                text=item.title,
                command=lambda it=item: self._show_item(it)
            )
            title_btn.pack(anchor="w")
            
            usage_label = ttk.Label(
                content_frame,
                text=f"{item.usage_count} mal verwendet | {item.category.title()}",
                font=("Arial", 9),
                foreground="gray"
            )
            usage_label.pack(anchor="w")
    
    def _show_recommendations(self):
        """Zeigt personalisierte Empfehlungen"""
        # Einfache Empfehlungen basierend auf aktueller Auswahl
        based_on = self.current_item.id if self.current_item else None
        recommendations = self.knowledge_engine.get_recommendations(based_on_item=based_on)
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        header_label = ttk.Label(
            self.content_frame,
            text="🎯 Empfehlungen für dich",
            font=("Arial", 16, "bold")
        )
        header_label.pack(pady=10)
        
        if based_on:
            context_label = ttk.Label(
                self.content_frame,
                text=f"Basierend auf: {self.current_item.title}",
                font=("Arial", 10),
                foreground="gray"
            )
            context_label.pack()
        
        if not recommendations:
            ttk.Label(
                self.content_frame,
                text="Keine spezifischen Empfehlungen verfügbar.",
                font=("Arial", 10),
                foreground="gray"
            ).pack(pady=20)
            return
        
        rec_frame = ttk.LabelFrame(self.content_frame, text="Empfohlene Features", padding=10)
        rec_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for item in recommendations:
            item_frame = ttk.Frame(rec_frame, relief="raised", borderwidth=1)
            item_frame.pack(fill="x", pady=5)
            
            title_btn = ttk.Button(
                item_frame,
                text=f"💡 {item.title}",
                command=lambda it=item: self._show_item(it)
            )
            title_btn.pack(fill="x", padx=5, pady=5)
            
            desc_label = ttk.Label(
                item_frame,
                text=item.description,
                font=("Arial", 9),
                foreground="gray",
                wraplength=500
            )
            desc_label.pack(padx=20, pady=(0, 5))
    
    def _show_statistics(self):
        """Zeigt Knowledge Base Statistiken"""
        stats = self.knowledge_engine.export_knowledge_summary()
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        header_label = ttk.Label(
            self.content_frame,
            text="📊 Knowledge Base Statistiken",
            font=("Arial", 16, "bold")
        )
        header_label.pack(pady=10)
        
        # Overview stats
        overview_frame = ttk.LabelFrame(self.content_frame, text="Übersicht", padding=10)
        overview_frame.pack(fill="x", padx=10, pady=5)
        
        overview_text = f"""
📄 Gesamt Features: {stats['total_items']}
📂 Kategorien: {stats['categories']}
🎓 Lernpfade: {stats['learning_paths']}
📅 Letztes Update: {stats['last_updated'][:10]}
        """.strip()
        
        ttk.Label(overview_frame, text=overview_text, font=("Arial", 10)).pack()
        
        # Category breakdown
        cat_frame = ttk.LabelFrame(self.content_frame, text="Kategorien-Aufschlüsselung", padding=10)
        cat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        for cat_id, cat_info in stats['categories_overview'].items():
            cat_info_frame = ttk.Frame(cat_frame)
            cat_info_frame.pack(fill="x", pady=2)
            
            ttk.Label(
                cat_info_frame,
                text=f"{cat_info['name']}: {cat_info['item_count']} Features",
                font=("Arial", 9, "bold")
            ).pack(side="left")
        
        # Popular items
        if stats['popular_items']:
            popular_frame = ttk.LabelFrame(self.content_frame, text="Meist genutzte Features", padding=10)
            popular_frame.pack(fill="x", padx=10, pady=5)
            
            for item_info in stats['popular_items']:
                ttk.Label(
                    popular_frame,
                    text=f"• {item_info['title']}: {item_info['usage']} mal genutzt",
                    font=("Arial", 9)
                ).pack(anchor="w")
    
    def _try_current_item(self):
        """Probiert das aktuelle Feature aus"""
        if not self.current_item:
            return
        
        # Extrahiere Aktion aus Beispielen
        if self.current_item.examples:
            example = self.current_item.examples[0]
            # Einfache Extraktion von Befehlen
            if "Sage:" in example:
                command = example.split("Sage:")[1].strip().strip("'\"")
                self.action_callback(command)
            else:
                # Fallback auf Feature-ID
                self.action_callback(self.current_item.id)
        else:
            self.action_callback(self.current_item.id)
    
    def _rate_current_item(self):
        """Bewertet das aktuelle Feature"""
        if not self.current_item:
            return
        
        # Einfaches Rating-Dialog
        rating_window = tk.Toplevel(self.center_window)
        rating_window.title("⭐ Feature bewerten")
        rating_window.geometry("300x150")
        rating_window.resizable(False, False)
        
        ttk.Label(rating_window, text=f"Bewerte: {self.current_item.title}", font=("Arial", 11, "bold")).pack(pady=10)
        
        rating_var = tk.DoubleVar(value=5.0)
        rating_scale = ttk.Scale(
            rating_window,
            from_=1.0,
            to=5.0,
            orient="horizontal",
            variable=rating_var,
            length=200
        )
        rating_scale.pack(pady=10)
        
        ttk.Label(rating_window, text="1 = Schlecht, 5 = Ausgezeichnet").pack()
        
        def submit_rating():
            self.knowledge_engine.rate_item(self.current_item.id, rating_var.get())
            self._update_details_panel(self.current_item)  # Refresh details
            rating_window.destroy()
        
        ttk.Button(rating_window, text="Bewertung abgeben", command=submit_rating).pack(pady=10)
