"""
Smart Suggestion Panel - Phase 5.1 GUI Component
Dynamisches Panel für adaptive KI-Vorschläge
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

from toobix.core.smart_suggestion_engine import SmartSuggestionEngine, SuggestionGroup, SuggestionContext

logger = logging.getLogger(__name__)

class SmartSuggestionPanel:
    """
    GUI Panel für Smart Suggestions mit dynamischen Buttons
    """
    
    def __init__(self, parent, suggestion_engine: SmartSuggestionEngine, action_callback: Callable[[str], None]):
        self.parent = parent
        self.suggestion_engine = suggestion_engine
        self.action_callback = action_callback
        
        self.suggestion_groups = []
        self.button_widgets = {}
        self.current_context = None
        
        self._create_panel()
        logger.info("🎯 Smart Suggestion Panel initialisiert")
    
    def _create_panel(self):
        """Erstellt das Suggestion Panel"""
        # Hauptframe für Suggestions
        if CTK_AVAILABLE:
            self.suggestion_frame = ctk.CTkFrame(self.parent)
            self.suggestion_frame.configure(fg_color=("gray90", "gray20"))
        else:
            self.suggestion_frame = ttk.LabelFrame(self.parent, text="💡 Smart Suggestions", padding=10)
        
        self.suggestion_frame.pack(fill="x", padx=5, pady=5)
        
        # Header
        self._create_header()
        
        # Scrollable content area
        self._create_content_area()
        
        # Footer mit Analytics
        self._create_footer()
    
    def _create_header(self):
        """Erstellt Header mit Titel und Controls"""
        if CTK_AVAILABLE:
            self.header_frame = ctk.CTkFrame(self.suggestion_frame)
            self.header_frame.configure(fg_color="transparent")
        else:
            self.header_frame = ttk.Frame(self.suggestion_frame)
        
        self.header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        if CTK_AVAILABLE:
            title_label = ctk.CTkLabel(
                self.header_frame, 
                text="💡 Smart Suggestions", 
                font=ctk.CTkFont(size=16, weight="bold")
            )
        else:
            title_label = ttk.Label(self.header_frame, text="💡 Smart Suggestions", font=("Arial", 12, "bold"))
        
        title_label.pack(side="left")
        
        # Refresh Button
        if CTK_AVAILABLE:
            refresh_btn = ctk.CTkButton(
                self.header_frame,
                text="🔄",
                width=30,
                height=25,
                command=self._refresh_suggestions
            )
        else:
            refresh_btn = ttk.Button(
                self.header_frame,
                text="🔄",
                width=3,
                command=self._refresh_suggestions
            )
        
        refresh_btn.pack(side="right")
        
        # Settings Button
        if CTK_AVAILABLE:
            settings_btn = ctk.CTkButton(
                self.header_frame,
                text="⚙️",
                width=30,
                height=25,
                command=self._show_suggestion_settings
            )
        else:
            settings_btn = ttk.Button(
                self.header_frame,
                text="⚙️",
                width=3,
                command=self._show_suggestion_settings
            )
        
        settings_btn.pack(side="right", padx=(0, 5))
    
    def _create_content_area(self):
        """Erstellt scrollbaren Content-Bereich"""
        if CTK_AVAILABLE:
            # CTK Scrollable Frame
            self.content_frame = ctk.CTkScrollableFrame(
                self.suggestion_frame,
                height=300,
                orientation="vertical"
            )
        else:
            # Standard Tkinter mit Scrollbar
            canvas = tk.Canvas(self.suggestion_frame, height=300)
            scrollbar = ttk.Scrollbar(self.suggestion_frame, orient="vertical", command=canvas.yview)
            self.content_frame = ttk.Frame(canvas)
            
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Update scroll region when content changes
            def _on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
            self.content_frame.bind("<Configure>", _on_frame_configure)
        
        self.content_frame.pack(fill="both", expand=True, pady=5)
        
        # Placeholder
        self._show_placeholder()
    
    def _create_footer(self):
        """Erstellt Footer mit Status und Analytics"""
        if CTK_AVAILABLE:
            self.footer_frame = ctk.CTkFrame(self.suggestion_frame)
            self.footer_frame.configure(fg_color="transparent")
        else:
            self.footer_frame = ttk.Frame(self.suggestion_frame)
        
        self.footer_frame.pack(fill="x", pady=(10, 0))
        
        # Status Label
        if CTK_AVAILABLE:
            self.status_label = ctk.CTkLabel(
                self.footer_frame, 
                text="Bereit für Vorschläge...",
                font=ctk.CTkFont(size=10)
            )
        else:
            self.status_label = ttk.Label(self.footer_frame, text="Bereit für Vorschläge...", font=("Arial", 8))
        
        self.status_label.pack(side="left")
        
        # Analytics Button
        if CTK_AVAILABLE:
            analytics_btn = ctk.CTkButton(
                self.footer_frame,
                text="📊 Analytics",
                width=80,
                height=20,
                font=ctk.CTkFont(size=10),
                command=self._show_analytics
            )
        else:
            analytics_btn = ttk.Button(
                self.footer_frame,
                text="📊",
                width=5,
                command=self._show_analytics
            )
        
        analytics_btn.pack(side="right")
    
    def _show_placeholder(self):
        """Zeigt Placeholder wenn keine Suggestions verfügbar"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if CTK_AVAILABLE:
            placeholder = ctk.CTkLabel(
                self.content_frame,
                text="🤖 Führe eine Unterhaltung um intelligente Vorschläge zu erhalten",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
        else:
            placeholder = ttk.Label(
                self.content_frame,
                text="🤖 Führe eine Unterhaltung um intelligente Vorschläge zu erhalten",
                font=("Arial", 10),
                foreground="gray"
            )
        
        placeholder.pack(pady=20)
    
    def update_suggestions(self, context: SuggestionContext):
        """Aktualisiert Suggestions basierend auf neuem Kontext"""
        try:
            self.current_context = context
            
            # Neue Suggestions generieren
            self.suggestion_groups = self.suggestion_engine.analyze_context(context)
            
            # GUI aktualisieren
            self._render_suggestions()
            
            # Status aktualisieren
            total_suggestions = sum(len(group.suggestions) for group in self.suggestion_groups)
            self.status_label.configure(text=f"{total_suggestions} Vorschläge in {len(self.suggestion_groups)} Kategorien")
            
        except Exception as e:
            logger.error(f"Suggestion Update Fehler: {e}")
            self._show_error("Fehler beim Laden der Vorschläge")
    
    def _render_suggestions(self):
        """Rendert alle Suggestion Groups"""
        # Clear existing content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        self.button_widgets.clear()
        
        if not self.suggestion_groups:
            self._show_placeholder()
            return
        
        # Render each group
        for i, group in enumerate(self.suggestion_groups):
            self._render_group(group, i)
    
    def _render_group(self, group: SuggestionGroup, index: int):
        """Rendert eine einzelne Suggestion Group"""
        # Group Header
        if CTK_AVAILABLE:
            group_frame = ctk.CTkFrame(self.content_frame)
            group_frame.configure(fg_color=("gray95", "gray25"))
        else:
            group_frame = ttk.LabelFrame(self.content_frame, text=group.name, padding=5)
        
        group_frame.pack(fill="x", pady=5, padx=5)
        
        if CTK_AVAILABLE:
            # Category Title for CTK
            title_label = ctk.CTkLabel(
                group_frame,
                text=f"📂 {group.name}",
                font=ctk.CTkFont(size=13, weight="bold")
            )
            title_label.pack(anchor="w", pady=(0, 5))
        
        # Suggestions Container
        if group.display_mode == 'buttons':
            self._render_buttons(group, group_frame)
        elif group.display_mode == 'dropdown':
            self._render_dropdown(group, group_frame)
        elif group.display_mode == 'grid':
            self._render_grid(group, group_frame)
    
    def _render_buttons(self, group: SuggestionGroup, parent):
        """Rendert Suggestions als Buttons"""
        button_frame = ttk.Frame(parent) if not CTK_AVAILABLE else ctk.CTkFrame(parent)
        if CTK_AVAILABLE:
            button_frame.configure(fg_color="transparent")
        button_frame.pack(fill="x", pady=2)
        
        visible_suggestions = group.suggestions[:group.max_visible]
        
        for suggestion in visible_suggestions:
            self._create_suggestion_button(suggestion, button_frame)
        
        # "More" button if there are hidden suggestions
        if len(group.suggestions) > group.max_visible:
            hidden_count = len(group.suggestions) - group.max_visible
            if CTK_AVAILABLE:
                more_btn = ctk.CTkButton(
                    button_frame,
                    text=f"... +{hidden_count} mehr",
                    width=100,
                    height=25,
                    font=ctk.CTkFont(size=10),
                    command=lambda: self._show_more_suggestions(group)
                )
            else:
                more_btn = ttk.Button(
                    button_frame,
                    text=f"... +{hidden_count} mehr",
                    command=lambda: self._show_more_suggestions(group)
                )
            
            more_btn.pack(side="left", padx=2)
    
    def _create_suggestion_button(self, suggestion, parent):
        """Erstellt einzelnen Suggestion Button"""
        button_text = f"{suggestion.icon} {suggestion.text}"
        
        if CTK_AVAILABLE:
            button = ctk.CTkButton(
                parent,
                text=button_text,
                width=120,
                height=30,
                command=lambda: self._execute_suggestion(suggestion),
                hover_color=("lightblue", "darkblue")
            )
        else:
            button = ttk.Button(
                parent,
                text=button_text,
                command=lambda: self._execute_suggestion(suggestion)
            )
        
        button.pack(side="left", padx=2, pady=2)
        
        # Tooltip
        self._create_tooltip(button, suggestion.tooltip)
        
        # Store for later reference
        self.button_widgets[suggestion.id] = button
    
    def _render_dropdown(self, group: SuggestionGroup, parent):
        """Rendert Suggestions als Dropdown"""
        dropdown_frame = ttk.Frame(parent) if not CTK_AVAILABLE else ctk.CTkFrame(parent)
        if CTK_AVAILABLE:
            dropdown_frame.configure(fg_color="transparent")
        dropdown_frame.pack(fill="x", pady=2)
        
        # Dropdown Variable
        selected_suggestion = tk.StringVar()
        suggestion_map = {}
        
        options = []
        for suggestion in group.suggestions:
            option_text = f"{suggestion.icon} {suggestion.text}"
            options.append(option_text)
            suggestion_map[option_text] = suggestion
        
        if CTK_AVAILABLE:
            dropdown = ctk.CTkComboBox(
                dropdown_frame,
                values=options,
                variable=selected_suggestion,
                width=200,
                command=lambda choice: self._execute_dropdown_suggestion(choice, suggestion_map)
            )
        else:
            dropdown = ttk.Combobox(
                dropdown_frame,
                values=options,
                textvariable=selected_suggestion,
                state="readonly",
                width=30
            )
            dropdown.bind("<<ComboboxSelected>>", 
                         lambda e: self._execute_dropdown_suggestion(selected_suggestion.get(), suggestion_map))
        
        dropdown.pack(side="left", padx=5)
        
        if options:
            dropdown.set("Wähle eine Aktion...")
    
    def _render_grid(self, group: SuggestionGroup, parent):
        """Rendert Suggestions als Grid"""
        grid_frame = ttk.Frame(parent) if not CTK_AVAILABLE else ctk.CTkFrame(parent)
        if CTK_AVAILABLE:
            grid_frame.configure(fg_color="transparent")
        grid_frame.pack(fill="x", pady=2)
        
        # Grid mit max 3 Spalten
        cols = 3
        for i, suggestion in enumerate(group.suggestions):
            row = i // cols
            col = i % cols
            
            button_text = f"{suggestion.icon}\n{suggestion.text}"
            
            if CTK_AVAILABLE:
                button = ctk.CTkButton(
                    grid_frame,
                    text=button_text,
                    width=80,
                    height=50,
                    command=lambda s=suggestion: self._execute_suggestion(s)
                )
            else:
                button = ttk.Button(
                    grid_frame,
                    text=button_text,
                    command=lambda s=suggestion: self._execute_suggestion(s)
                )
            
            button.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            
            # Configure grid weights
            grid_frame.grid_columnconfigure(col, weight=1)
    
    def _execute_suggestion(self, suggestion):
        """Führt eine Suggestion aus"""
        try:
            # Feedback an Suggestion Engine
            self.suggestion_engine.update_user_feedback(suggestion.id, 'clicked')
            
            # Button visuelles Feedback
            if suggestion.id in self.button_widgets:
                button = self.button_widgets[suggestion.id]
                original_text = button.cget("text")
                
                if CTK_AVAILABLE:
                    button.configure(text=f"✅ {original_text}")
                else:
                    button.configure(text=f"✅ {original_text}")
                
                # Nach 2 Sekunden zurücksetzen
                button.after(2000, lambda: button.configure(text=original_text))
            
            # Action ausführen
            self.action_callback(suggestion.action)
            
            logger.info(f"Suggestion ausgeführt: {suggestion.text} -> {suggestion.action}")
            
        except Exception as e:
            logger.error(f"Suggestion Execution Fehler: {e}")
            self._show_error(f"Fehler bei Aktion: {e}")
    
    def _execute_dropdown_suggestion(self, choice: str, suggestion_map: Dict[str, Any]):
        """Führt Dropdown-Suggestion aus"""
        if choice in suggestion_map:
            self._execute_suggestion(suggestion_map[choice])
    
    def _create_tooltip(self, widget, text: str):
        """Erstellt Tooltip für Widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                background="lightyellow",
                relief="solid",
                borderwidth=1,
                font=("Arial", 9)
            )
            label.pack()
            
            # Auto-hide nach 3 Sekunden
            tooltip.after(3000, tooltip.destroy)
        
        def hide_tooltip(event):
            # Tooltip wird automatisch versteckt
            pass
        
        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)
    
    def _refresh_suggestions(self):
        """Aktualisiert Suggestions manuell"""
        if self.current_context:
            self.update_suggestions(self.current_context)
            self.status_label.configure(text="Vorschläge aktualisiert")
    
    def _show_suggestion_settings(self):
        """Zeigt Suggestion-Einstellungen"""
        settings_window = tk.Toplevel(self.parent)
        settings_window.title("Smart Suggestion Einstellungen")
        settings_window.geometry("400x300")
        
        # TODO: Implementiere Settings-GUI
        label = ttk.Label(settings_window, text="🚧 Einstellungen kommen in Phase 5.2")
        label.pack(pady=50)
    
    def _show_analytics(self):
        """Zeigt Suggestion Analytics"""
        analytics = self.suggestion_engine.get_suggestion_analytics()
        
        analytics_window = tk.Toplevel(self.parent)
        analytics_window.title("📊 Suggestion Analytics")
        analytics_window.geometry("500x400")
        
        # Analytics Text
        text_widget = tk.Text(analytics_window, wrap="word", padx=10, pady=10)
        text_widget.pack(fill="both", expand=True)
        
        analytics_text = "📊 SMART SUGGESTION ANALYTICS\n\n"
        
        if 'error' in analytics:
            analytics_text += f"❌ {analytics['error']}\n"
        else:
            analytics_text += f"🎯 Generierte Vorschläge gesamt: {analytics['total_suggestions_generated']}\n"
            analytics_text += f"📊 Durchschnittliche Gruppen: {analytics['average_groups_per_session']:.1f}\n"
            analytics_text += f"🔄 Suggestion-Sessions: {analytics['suggestion_frequency']}\n\n"
            
            analytics_text += "📈 BELIEBTE KATEGORIEN:\n"
            for category, count in analytics['most_common_categories'].items():
                analytics_text += f"  • {category}: {count}x\n"
            
            analytics_text += "\n🎯 BENUTZER-PRÄFERENZEN:\n"
            for suggestion_id, preference in list(analytics['user_preference_trends'].items())[:5]:
                analytics_text += f"  • {suggestion_id}: {preference:.2f}\n"
        
        text_widget.insert("1.0", analytics_text)
        text_widget.configure(state="disabled")
    
    def _show_more_suggestions(self, group: SuggestionGroup):
        """Zeigt alle Suggestions einer Gruppe"""
        more_window = tk.Toplevel(self.parent)
        more_window.title(f"Alle {group.name} Vorschläge")
        more_window.geometry("400x300")
        
        # Scrollable list
        canvas = tk.Canvas(more_window)
        scrollbar = ttk.Scrollbar(more_window, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Add all suggestions as buttons
        for suggestion in group.suggestions:
            button = ttk.Button(
                scrollable_frame,
                text=f"{suggestion.icon} {suggestion.text}",
                command=lambda s=suggestion: [self._execute_suggestion(s), more_window.destroy()]
            )
            button.pack(fill="x", pady=2, padx=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Update scroll region
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def _show_error(self, message: str):
        """Zeigt Fehlermeldung"""
        self.status_label.configure(text=f"❌ {message}")
        
        # Nach 5 Sekunden zurücksetzen
        self.status_label.after(5000, lambda: self.status_label.configure(text="Bereit für Vorschläge..."))
    
    def hide_panel(self):
        """Versteckt das Panel"""
        self.suggestion_frame.pack_forget()
    
    def show_panel(self):
        """Zeigt das Panel"""
        self.suggestion_frame.pack(fill="x", padx=5, pady=5)
    
    def get_widget(self):
        """Gibt das Haupt-Widget zurück"""
        return self.suggestion_frame
