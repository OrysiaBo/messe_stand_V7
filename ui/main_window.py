#!/usr/bin/env python3
"""
Main Window für Dynamic Messe Stand V4
Haupt-GUI-Fenster mit responsivem Design
"""

import tkinter as tk
from tkinter import ttk
import sys
import subprocess
from core.config import config
from core.theme import theme_manager, THEME_VARS, _mix
from core.logger import logger
from ui.components.header import HeaderComponent
from ui.components.status_panel import StatusPanelComponent
from ui.components.footer import FooterComponent
from ui.tabs.home_tab import HomeTab
from ui.tabs.creator_tab import CreatorTab
from ui.tabs.presentation_tab import PresentationTab

class MainWindow:
    """Haupt-GUI-Fenster"""
    
    def __init__(self, esp32_port=None):
        logger.info("🚀 Starte Dynamic Messe Stand V4...")
        
        # Tkinter Root
        self.root = tk.Tk()
        self.root.title(config.gui['title'])
        
        # Basis-Variablen
        self.esp32_port = esp32_port
        self.fullscreen = False
        self.current_tab = "home"
        
        # Setup
        self.setup_window()
        self.setup_responsive_design()
        self.setup_styles()
        self.setup_gui_components()
        self.setup_tabs()
        
        # Initialer Tab
        self.switch_tab("home")
        
        logger.info("✅ Dynamic Messe Stand V4 erfolgreich initialisiert!")
        self.setup_content_synchronization()

def setup_content_synchronization(self):
    """Налаштовує синхронізацію контенту між табами"""
    try:
        from models.content import content_manager
        
        # Підписати MainWindow на зміни контенту
        content_manager.add_observer(self.on_content_changed)
        
        logger.debug("Content synchronization setup complete")
        
    except Exception as e:
        logger.error(f"Error setting up content synchronization: {e}")

def on_content_changed(self, slide_id, slide_data, action='update'):
    """Обробник змін контенту для синхронізації всіх табів"""
    try:
        # Синхронізувати Demo Tab
        if hasattr(self, 'demo_tab'):
            # Demo tab має власний обробник, він автоматично оновиться
            pass
        
        # Синхронізувати Creator Tab
        if hasattr(self, 'creator_tab'):
            # Оновити thumbnails в Creator
            if hasattr(self.creator_tab, 'create_slide_thumbnails'):
                self.creator_tab.create_slide_thumbnails()
        
        # Синхронізувати Home Tab якщо є
        if hasattr(self, 'home_tab'):
            if hasattr(self.home_tab, 'refresh_content'):
                self.home_tab.refresh_content()
        
        logger.debug(f"All tabs synchronized for slide {slide_id} change")
        
    except Exception as e:
        logger.error(f"Error synchronizing tabs: {e}")

def refresh_all_tabs(self):
    """Примусово оновлює всі таби після завантаження презентації"""
    try:
        # Оновити Demo Tab
        if hasattr(self, 'demo_tab'):
            if hasattr(self.demo_tab, 'create_slides_list'):
                self.demo_tab.create_slides_list()
            if hasattr(self.demo_tab, 'load_current_slide'):
                self.demo_tab.load_current_slide()
        
        # Оновити Creator Tab
        if hasattr(self, 'creator_tab'):
            if hasattr(self.creator_tab, 'create_slide_thumbnails'):
                self.creator_tab.create_slide_thumbnails()
            if hasattr(self.creator_tab, 'load_slide_to_editor'):
                # Перезавантажити поточний слайд
                current_slide = getattr(self.creator_tab, 'current_edit_slide', 1)
                self.creator_tab.load_slide_to_editor(current_slide)
        
        # Оновити Home Tab
        if hasattr(self, 'home_tab'):
            if hasattr(self.home_tab, 'refresh_content'):
                self.home_tab.refresh_content()
        
        logger.info("All tabs refreshed successfully")
        
    except Exception as e:
        logger.error(f"Error refreshing all tabs: {e}")

def switch_tab(self, tab_name):
    """Переключення між табами з автоматичним збереженням"""
    try:
        # Зберегти поточні зміни в Creator перед переключенням
        if (hasattr(self, 'creator_tab') and 
            hasattr(self.creator_tab, 'save_current_slide_content') and
            self.current_tab == 'creator'):
            self.creator_tab.save_current_slide_content()
        
        # ... існуючий код переключення табів ...
        
        # Оновити контент в новому табі
        if tab_name == 'demo' and hasattr(self, 'demo_tab'):
            if hasattr(self.demo_tab, 'load_current_slide'):
                self.demo_tab.load_current_slide()
        elif tab_name == 'creator' and hasattr(self, 'creator_tab'):
            if hasattr(self.creator_tab, 'load_slide_to_editor'):
                current_slide = getattr(self.creator_tab, 'current_edit_slide', 1)
                self.creator_tab.load_slide_to_editor(current_slide)
        
        # Оновити header navigation
        if hasattr(self, 'header'):
            if hasattr(self.header, 'update_active_tab'):
                self.header.update_active_tab(tab_name)
        
        self.current_tab = tab_name
        logger.debug(f"Switched to {tab_name} tab with synchronization")
        
    except Exception as e:
        logger.error(f"Error switching to {tab_name} tab: {e}")

# ДОДАТИ ТАКОЖ ДО КЛАСУ HeaderComponent в ui/components/header.py

def save_presentation_json(self):
    """Зберігає презентацію як JSON з попереднім збереженням змін"""
    try:
        # Зберегти поточні зміни в Creator якщо активний
        if (hasattr(self.main_window, 'current_tab') and 
            self.main_window.current_tab == 'creator' and
            hasattr(self.main_window, 'creator_tab')):
            if hasattr(self.main_window.creator_tab, 'save_current_slide_content'):
                self.main_window.creator_tab.save_current_slide_content()
        
        # Зберегти через content_manager
        from models.content import content_manager
        filename = content_manager.export_presentation_as_json()
        if filename:
            logger.info(f"Презентацію збережено як JSON: {filename}")
            self.show_save_success("JSON")
        else:
            raise Exception("Не вдалося зберегти файл")
            
    except Exception as e:
        logger.error(f"Помилка при збереженні JSON: {e}")
        from tkinter import messagebox
        messagebox.showerror("Помилка збереження", f"Не вдалося зберегти презентацію:\n{e}")

def save_presentation_yaml(self):
    """Зберігає презентацію як YAML з попереднім збереженням змін"""
    try:
        # Зберегти поточні зміни в Creator якщо активний
        if (hasattr(self.main_window, 'current_tab') and 
            self.main_window.current_tab == 'creator' and
            hasattr(self.main_window, 'creator_tab')):
            if hasattr(self.main_window.creator_tab, 'save_current_slide_content'):
                self.main_window.creator_tab.save_current_slide_content()
        
        # Зберегти через content_manager
        from models.content import content_manager
        filename = content_manager.export_presentation_as_yaml()
        if filename:
            logger.info(f"Презентацію збережено як YAML: {filename}")
            self.show_save_success("YAML")
        else:
            raise Exception("Не вдалося зберегти файл")
            
    except Exception as e:
        logger.error(f"Помилка при збереженні YAML: {e}")
        from tkinter import messagebox
        messagebox.showerror("Помилка збереження", f"Не вдалося зберегти презентацію:\n{e}")

def load_presentation(self):
    """Завантажує презентацію з синхронізацією всіх табів"""
    try:
        from models.content import content_manager
        success = content_manager.load_presentation_from_file()
        if success:
            logger.info("Презентацію завантажено успішно")
            self.show_load_success()
            
            # Синхронізувати всі таби
            if hasattr(self.main_window, 'refresh_all_tabs'):
                self.main_window.refresh_all_tabs()
        else:
            logger.warning("Не вдалося завантажити презентацію")
            
    except Exception as e:
        logger.error(f"Помилка при завантаженні презентації: {e}")
        from tkinter import messagebox
        messagebox.showerror("Помилка завантаження", f"Не вдалося завантажити презентацію:\n{e}")
    
    def setup_window(self):
        """Konfiguriert das Hauptfenster für 24" RTC Monitor"""
        # Hauptmonitor ermitteln (primärer Monitor)
        self.detect_primary_monitor()
        
        # Für 24" RTC Monitor optimiert
        self.window_width = self.primary_width
        self.window_height = self.primary_height
        
        logger.info(f"Hauptmonitor erkannt: {self.window_width}x{self.window_height} bei ({self.primary_x}, {self.primary_y})")
        
        # Fenster explizit auf Hauptmonitor positionieren
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.primary_x}+{self.primary_y}")
        self.root.minsize(config.gui['min_width'], config.gui['min_height'])
        
        # Vollbild-Bindings
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        # Sofort in Vollbild auf Hauptmonitor
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)  # Immer im Vordergrund
        self.fullscreen = True
        
        # Fenster auf Hauptmonitor forcieren
        self.root.wm_attributes('-zoomed', True)  # Linux maximieren
        self.root.focus_force()    # Fokus erzwingen
        self.root.lift()           # Fenster nach vorne bringen
        
        # Sicherstellen, dass Fenster auf Hauptmonitor bleibt
        self.root.after(100, self.ensure_primary_monitor)
        
        # Theme anwenden
        colors = theme_manager.get_colors()
        self.root.configure(bg=colors['background_primary'])
    
    def detect_primary_monitor(self):
        """Erkennt den primären Monitor (Hauptbildschirm)"""
        try:
            # Tkinter-Methode für primären Monitor
            self.root.update_idletasks()
            
            # Gesamte Bildschirmgröße
            total_width = self.root.winfo_screenwidth()
            total_height = self.root.winfo_screenheight()
            
            # Primärer Monitor ist normalerweise bei (0,0)
            self.primary_x = 0
            self.primary_y = 0
            self.primary_width = total_width
            self.primary_height = total_height
            
            # Versuche Multi-Monitor Setup zu erkennen
            try:
                import subprocess
                result = subprocess.run(['xrandr'], capture_output=True, text=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if ' connected primary ' in line:
                            # Primärer Monitor gefunden
                            parts = line.split()
                            for part in parts:
                                if 'x' in part and '+' in part:
                                    # Format: 1920x1080+0+0
                                    resolution_pos = part.split('+')
                                    if len(resolution_pos) >= 3:
                                        resolution = resolution_pos[0]
                                        self.primary_x = int(resolution_pos[1])
                                        self.primary_y = int(resolution_pos[2])
                                        
                                        if 'x' in resolution:
                                            w, h = resolution.split('x')
                                            self.primary_width = int(w)
                                            self.primary_height = int(h)
                                    break
                            break
            except:
                pass  # Fallback auf Standard-Werte
            
            logger.info(f"Primärer Monitor: {self.primary_width}x{self.primary_height} bei ({self.primary_x}, {self.primary_y})")
            
        except Exception as e:
            logger.warning(f"Monitor-Erkennung fehlgeschlagen: {e}")
            # Fallback-Werte
            self.primary_x = 0
            self.primary_y = 0
            self.primary_width = 1920
            self.primary_height = 1080
    
    def ensure_primary_monitor(self):
        """Stellt sicher, dass das Fenster auf dem Hauptmonitor bleibt"""
        try:
            # Fenster-Position prüfen und korrigieren
            current_x = self.root.winfo_x()
            current_y = self.root.winfo_y()
            
            # Falls Fenster nicht auf Hauptmonitor, zurück bewegen
            if current_x != self.primary_x or current_y != self.primary_y:
                self.root.geometry(f"{self.primary_width}x{self.primary_height}+{self.primary_x}+{self.primary_y}")
                logger.info(f"Fenster auf Hauptmonitor zurück bewegt: ({self.primary_x}, {self.primary_y})")
            
        except Exception as e:
            logger.warning(f"Monitor-Korrektur fehlgeschlagen: {e}")
    
    def setup_responsive_design(self):
        """Konfiguriert responsive Design-Elemente"""
        # Scale Factor für responsive Design
        self.scale_factor = min(self.window_width, self.window_height) / config.design['scale_factor_base']
        
        # Responsive Schriftarten
        self.fonts = theme_manager.get_fonts(self.window_width, self.window_height)
        
        logger.debug(f"Responsive Design: {self.window_width}x{self.window_height}, Scale: {self.scale_factor:.2f}")
    
    def setup_styles(self):
        """Wendet das komplette Bertrandt Dark Theme an - überschreibt alle anderen Styles"""
        # Bertrandt Dark Theme direkt anwenden
        from core.theme import apply_bertrandt_dark_theme
        apply_bertrandt_dark_theme(self.root, reapply=True)
        self.style = ttk.Style()
        
        # Zusätzliche moderne Styles für bessere Integration
        colors = theme_manager.get_colors()
        spacing = theme_manager.get_spacing()
        
        # Überschreibe alle Standard-Styles mit Bertrandt Theme
        # Frames
        self.style.configure('TFrame', 
                           background=THEME_VARS["bg"],
                           relief='flat',
                           borderwidth=0)
        
        # Labels - alle mit Bertrandt Farben
        self.style.configure('TLabel',
                           background=THEME_VARS["bg"],
                           foreground=THEME_VARS["text"],
                           font=(THEME_VARS["font_family"], THEME_VARS["size_body"]))
        
        # Buttons - alle mit Bertrandt Styles
        self.style.configure('TButton',
                           background=THEME_VARS["brand_600"],
                           foreground="#ffffff",
                           font=(THEME_VARS["font_family"], THEME_VARS["size_body"], "bold"),
                           relief='flat',
                           borderwidth=0,
                           padding=(THEME_VARS["pad"], THEME_VARS["pad"] // 2))
        
        # Entry - alle mit Bertrandt Styles
        self.style.configure('TEntry',
                           fieldbackground=THEME_VARS["panel"],
                           foreground=THEME_VARS["text"],
                           bordercolor=THEME_VARS["border"],
                           relief='flat',
                           borderwidth=1,
                           padding=THEME_VARS["pad"])
        
        # Notebook - alle mit Bertrandt Styles
        self.style.configure('TNotebook',
                           background=THEME_VARS["bg"],
                           borderwidth=0)
        
        self.style.configure('TNotebook.Tab',
                           background=THEME_VARS["panel"],
                           foreground=THEME_VARS["text"],
                           bordercolor=THEME_VARS["border"],
                           padding=(THEME_VARS["pad"], THEME_VARS["pad"] // 2))
        
        # Alle anderen Widgets überschreiben
        self.style.configure('TCheckbutton', background=THEME_VARS["bg"], foreground=THEME_VARS["text"])
        self.style.configure('TRadiobutton', background=THEME_VARS["bg"], foreground=THEME_VARS["text"])
        self.style.configure('TCombobox', fieldbackground=THEME_VARS["panel"], foreground=THEME_VARS["text"])
        self.style.configure('TSpinbox', fieldbackground=THEME_VARS["panel"], foreground=THEME_VARS["text"])
        self.style.configure('TScale', background=THEME_VARS["bg"], troughcolor=THEME_VARS["panel"])
        self.style.configure('TSeparator', background=THEME_VARS["border"])
        self.style.configure('TScrollbar', background=THEME_VARS["panel"], troughcolor=THEME_VARS["bg"])
        
        # Progressbar mit Bertrandt Blau
        self.style.configure('TProgressbar',
                           background=THEME_VARS["brand_600"],
                           troughcolor=THEME_VARS["panel"],
                           bordercolor=THEME_VARS["border"])
        
        # Treeview mit Bertrandt Theme
        self.style.configure('Treeview',
                           background=THEME_VARS["panel"],
                           foreground=THEME_VARS["text"],
                           fieldbackground=THEME_VARS["panel"],
                           bordercolor=THEME_VARS["border"])
        
        self.style.configure('Treeview.Heading',
                           background=THEME_VARS["panel_2"],
                           foreground=THEME_VARS["text"],
                           relief='flat')
        
        # Listbox Style
        self.style.configure('TListbox',
                           background=THEME_VARS["panel"],
                           foreground=THEME_VARS["text"],
                           selectbackground=THEME_VARS["brand_600"],
                           selectforeground="#ffffff")
        
        # Text Widget Style
        self.style.configure('TText',
                           background=THEME_VARS["panel"],
                           foreground=THEME_VARS["text"],
                           insertbackground=THEME_VARS["text"],
                           selectbackground=THEME_VARS["brand_600"],
                           selectforeground="#ffffff")
        
        # Menu Styles
        self.style.configure('TMenu',
                           background=THEME_VARS["panel"],
                           foreground=THEME_VARS["text"],
                           selectcolor=THEME_VARS["brand_600"])
        
        self.style.configure('TMenubutton',
                           background=THEME_VARS["panel"],
                           foreground=THEME_VARS["text"],
                           bordercolor=THEME_VARS["border"])
        
        # Panedwindow
        self.style.configure('TPanedwindow',
                           background=THEME_VARS["bg"])
        
        # Sizegrip
        self.style.configure('TSizegrip',
                           background=THEME_VARS["bg"])
        
        # Tooltip Style
        self.style.configure('TTooltip',
                           background=THEME_VARS["panel_2"],
                           foreground=THEME_VARS["text"],
                           bordercolor=THEME_VARS["border"])
        
        # Alle Map-States für Hover-Effekte überschreiben
        for widget_type in ['TButton', 'TCheckbutton', 'TRadiobutton', 'TCombobox', 'TSpinbox', 'TMenubutton']:
            self.style.map(widget_type,
                          background=[('active', THEME_VARS["brand_400"]),
                                    ('pressed', THEME_VARS["brand_700"]),
                                    ('disabled', THEME_VARS["panel_2"])],
                          foreground=[('disabled', THEME_VARS["muted"])])
        
        # Tab-Map für Notebook
        self.style.map('TNotebook.Tab',
                      background=[('selected', THEME_VARS["panel_2"]),
                                ('active', _mix(THEME_VARS["panel"], THEME_VARS["brand_600"], 0.12))],
                      foreground=[('selected', THEME_VARS["text"])])
    
    def setup_gui_components(self):
        """Erstellt die Bertrandt Layout-Struktur nach Referenz"""
        # Hauptcontainer mit Bertrandt Padding (14px)
        self.main_container = ttk.Frame(self.root, style="TFrame")
        self.main_container.pack(fill='both', expand=True, padx=14, pady=12)
        
        # Navbar (Glass-Frame oben) - nach Bertrandt Referenz
        self.navbar = ttk.Frame(self.main_container, style="Glass.TFrame", padding=(12, 10))
        self.navbar.pack(side="top", fill="x", pady=(0, 12))
        self.setup_navbar()
        
        # Hero-Bereich (große Karte) - nach Bertrandt Referenz
        self.hero_outer, self.hero = self.make_glass_card(self.main_container, padding=16)
        self.hero_outer.pack(fill="x", pady=(0, 12))
        self.setup_hero()
        
        # Grid-Container (3-Spalten-Layout) - nach Bertrandt Referenz
        self.grid_container = ttk.Frame(self.main_container, style="TFrame")
        self.grid_container.pack(fill="both", expand=True, pady=(0, 12))
        self.grid_container.columnconfigure((0,1,2), weight=1)
        self.grid_container.rowconfigure((0,1), weight=1)
        
        # Content-Bereich für Tabs - nimmt das komplette Grid ein
        self.content_frame = self.grid_container
        self.tab_content_frame = self.grid_container
        
        # Footer mit Separator - nach Bertrandt Referenz
        self.footer_frame = ttk.Frame(self.main_container, style="TFrame")
        self.footer_frame.pack(side="bottom", fill="x")
        ttk.Separator(self.footer_frame).pack(fill="x", pady=6)
        self.footer_label = ttk.Label(
            self.footer_frame, 
            text="© 2025 Bertrandt AG - Dynamic Messe Stand V4 - Marvin Mayer", 
            style="Muted.TLabel"
        )
        self.footer_label.pack()
        
        logger.info("✅ Bertrandt Layout-Struktur erstellt")
    
    def make_glass_card(self, parent, padding=12):
        """Erstellt eine Glass-Card im Bertrandt-Style"""
        from core.theme import THEME_VARS, _mix
        
        # Outer Frame
        outer = ttk.Frame(parent, style="TFrame")
        
        # Canvas für Hintergrund-Effekt
        cv = tk.Canvas(outer, bg=THEME_VARS["bg"], highlightthickness=0, bd=0, height=1)
        cv.grid(row=0, column=0, sticky="nsew")
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)
        
        # Inner Frame mit Glass-Style
        inner = ttk.Frame(outer, style="Glass.TFrame", padding=padding)
        inner.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Redraw-Funktion für Glass-Effekt
        def _redraw(_evt=None):
            cv.delete("all")
            w = outer.winfo_width()
            h = outer.winfo_height()
            if w < 2 or h < 2: 
                return
            # Simulierte Kontur
            cv.create_rectangle(
                1, 1, w-2, h-2,
                outline=THEME_VARS["elev_outline"],
                width=1
            )
            # Leichte Innenfläche ("Glas")
            cv.create_rectangle(
                2, 2, w-3, h-3,
                outline="",
                fill=_mix(THEME_VARS["panel"], "#ffffff", 0.04)
            )
        
        outer.bind("<Configure>", _redraw)
        return outer, inner
    
    def setup_navbar(self):
        """Erstellt die Navbar nach Bertrandt Referenz"""
        # Left side - Brand Badge + Title
        left_frame = ttk.Frame(self.navbar, style="TFrame")
        left_frame.pack(side="left")
        
        # Bertrandt Logo
        self.load_logo(left_frame)
        
        # Title
        title_label = ttk.Label(left_frame, text="Dynamic Messe Stand V4", style="H2.TLabel")
        title_label.pack(side="left")
        
        # Right side - Navigation Buttons
        right_frame = ttk.Frame(self.navbar, style="TFrame")
        right_frame.pack(side="right")
        
        # Navigation Buttons
        nav_buttons = [
            ("Home", "home"),
            ("Demo", "demo"), 
            ("Creator", "creator"),
            ("Presentation", "presentation")
        ]
        
        self.nav_buttons = {}
        for text, tab_name in nav_buttons:
            btn = ttk.Button(
                right_frame, 
                text=text, 
                style="Ghost.TButton",
                command=lambda t=tab_name: self.switch_tab(t)
            )
            btn.pack(side="left", padx=6)
            self.nav_buttons[tab_name] = btn
        
        # Theme Toggle Button
        theme_btn = ttk.Button(
            right_frame, 
            text="🌙", 
            style="Ghost.TButton",
            command=self.toggle_theme
        )
        theme_btn.pack(side="left", padx=6)
        
        # Primary Action Button
        primary_btn = ttk.Button(
            right_frame, 
            text="System Status", 
            style="Primary.TButton",
            command=self.show_system_status
        )
        primary_btn.pack(side="left", padx=6)
    
    def setup_hero(self):
        """Erstellt den Hero-Bereich nach Bertrandt Referenz"""
        # Eyebrow Text
        eyebrow = ttk.Label(
            self.hero, 
            text="Interaktives Messestand-System", 
            foreground=_mix(THEME_VARS["brand_600"], "#9cc7fb", 0.5)
        )
        eyebrow.pack(anchor="w")
        
        # Main Title
        title = ttk.Label(
            self.hero, 
            text="Bertrandt Dynamic Messe Stand V4", 
            style="H1.TLabel"
        )
        title.pack(anchor="w", pady=(4, 4))
        
        # Description
        description = ttk.Label(
            self.hero, 
            text="Professionelles Touch-Interface für interaktive Messestände mit Hardware-Integration und Live-Demos.", 
            style="Muted.TLabel", 
            wraplength=900, 
            justify="left"
        )
        description.pack(anchor="w")
    
    def load_logo(self, parent_frame):
        """Lädt das passende Logo basierend auf dem aktuellen Theme"""
        try:
            from PIL import Image, ImageTk
            from core.theme import get_logo_filename
            import os
            
            # Logo-Dateiname basierend auf Theme
            logo_filename = get_logo_filename()
            logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", logo_filename)
            
            # Logo laden und skalieren
            logo_image = Image.open(logo_path)
            
            # Logo auf passende Größe skalieren (Höhe: 28px, Breite proportional)
            logo_height = 28
            logo_width = int((logo_image.width * logo_height) / logo_image.height)
            logo_image = logo_image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # PhotoImage erstellen
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            
            # Logo Label erstellen oder aktualisieren
            if hasattr(self, 'logo_label'):
                self.logo_label.configure(image=self.logo_photo)
            else:
                self.logo_label = ttk.Label(parent_frame, image=self.logo_photo, style="TLabel")
                self.logo_label.pack(side="left", padx=(0, 10))
            
        except Exception as e:
            logger.warning(f"Bertrandt Logo konnte nicht geladen werden: {e}")
            # Fallback: Canvas Badge
            if not hasattr(self, 'logo_badge'):
                self.logo_badge = tk.Canvas(parent_frame, width=28, height=28, bg=THEME_VARS["panel"], highlightthickness=0)
                self.logo_badge.pack(side="left", padx=(0, 10))
            
            self.logo_badge.configure(bg=THEME_VARS["panel"])
            self.logo_badge.delete("all")
            self.logo_badge.create_rectangle(2, 2, 26, 26, outline="", fill=_mix(THEME_VARS["brand_600"], THEME_VARS["brand_500"], 0.5))

    def toggle_theme(self):
        """Wechselt zwischen Dark und Light Theme"""
        from core.theme import toggle_theme, apply_bertrandt_theme
        
        # Theme wechseln
        new_theme = toggle_theme()
        
        # Theme auf die Anwendung anwenden
        apply_bertrandt_theme(self.root, reapply=True)
        
        # Styles neu anwenden
        self.setup_styles()
        
        # Logo neu laden
        if hasattr(self, 'logo_label'):
            parent = self.logo_label.master
            self.load_logo(parent)
        
        # Alle Tabs über Theme-Wechsel benachrichtigen
        self.refresh_all_tabs()
        
        # Toast anzeigen
        from core.theme import _toast
        theme_name = "Hell" if new_theme == "light" else "Dunkel"
        _toast(self.root, f"Theme gewechselt: {theme_name}")
        
        logger.info(f"Theme gewechselt zu: {new_theme}")
    
    def toggle_low_color(self):
        """Wechselt den Low-Color Modus für bessere Sichtbarkeit"""
        from core.theme import toggle_low_color, apply_bertrandt_theme, LOW_COLOR_MODE
        
        # Low-Color Modus wechseln
        new_mode = toggle_low_color()
        
        # Theme auf die Anwendung anwenden
        apply_bertrandt_theme(self.root, reapply=True)
        
        # Styles neu anwenden
        self.setup_styles()
        
        # Alle Tabs über Theme-Wechsel benachrichtigen
        self.refresh_all_tabs()
        
        # Toast anzeigen
        from core.theme import _toast
        mode_name = "Ein" if new_mode else "Aus"
        _toast(self.root, f"Low-Color Modus: {mode_name}")
        
        logger.info(f"Low-Color Modus: {mode_name}")
    
    def refresh_all_tabs(self):
        """Aktualisiert alle Tabs nach einem Theme-Wechsel oder Präsentations-Import"""
        for tab_name, tab in self.tabs.items():
            # Theme-Updates
            if hasattr(tab, 'refresh_theme'):
                try:
                    tab.refresh_theme()
                    logger.debug(f"Theme für {tab_name}-Tab aktualisiert")
                except Exception as e:
                    logger.warning(f"Fehler beim Theme-Update für {tab_name}: {e}")
            
            # Content-Updates nach Präsentations-Import
            if hasattr(tab, 'refresh_thumbnails'):
                try:
                    tab.refresh_thumbnails()
                    logger.debug(f"Thumbnails für {tab_name}-Tab aktualisiert")
                except Exception as e:
                    logger.warning(f"Fehler beim Thumbnail-Update für {tab_name}: {e}")
            
            if hasattr(tab, 'create_demo_thumbnails'):
                try:
                    tab.create_demo_thumbnails()
                    logger.debug(f"Demo-Thumbnails für {tab_name}-Tab aktualisiert")
                except Exception as e:
                    logger.warning(f"Fehler beim Demo-Thumbnail-Update für {tab_name}: {e}")
            
            if hasattr(tab, 'update_slide_display'):
                try:
                    tab.update_slide_display(1)  # Zur ersten Slide
                    logger.debug(f"Slide-Display für {tab_name}-Tab aktualisiert")
                except Exception as e:
                    logger.warning(f"Fehler beim Slide-Display-Update für {tab_name}: {e}")
        
        # Demo-Service zurücksetzen
        try:
            from services.demo import demo_service
            if hasattr(demo_service, 'reset_to_first_slide'):
                demo_service.reset_to_first_slide()
            logger.debug("Demo-Service nach Präsentations-Import zurückgesetzt")
        except Exception as e:
            logger.warning(f"Fehler beim Demo-Service-Reset: {e}")

    def show_system_status(self):
        """Zeigt System-Status in einem Toast"""
        from core.theme import _toast
        _toast(self.root, "System läuft optimal - Alle Verbindungen aktiv")
    
    def update_navbar_active_tab(self, active_tab):
        """Aktualisiert die aktive Tab-Anzeige in der Navbar"""
        for tab_name, button in self.nav_buttons.items():
            if tab_name == active_tab:
                button.configure(style="Primary.TButton")
            else:
                button.configure(style="Ghost.TButton")
    
    def setup_tabs(self):
        """Initialisiert alle Tab-Komponenten"""
        self.tabs = {
            'home': HomeTab(self.tab_content_frame, self),
            'demo': DemoTab(self.tab_content_frame, self),
            'creator': CreatorTab(self.tab_content_frame, self),
            'presentation': PresentationTab(self.tab_content_frame, self)
        }
        
        # Alle Tabs initial verstecken
        for tab in self.tabs.values():
            tab.hide()
    
    def switch_tab(self, tab_name):
        """Wechselt zwischen Tabs"""
        if tab_name not in self.tabs:
            logger.error(f"Unbekannter Tab: {tab_name}")
            return False
        
        # Aktuellen Tab verstecken
        if self.current_tab in self.tabs:
            self.tabs[self.current_tab].hide()
        
        # Neuen Tab anzeigen
        self.tabs[tab_name].show()
        self.current_tab = tab_name
        
        # Navbar-Navigation aktualisieren
        self.update_navbar_active_tab(tab_name)
        
        logger.debug(f"Tab gewechselt: {tab_name}")
        return True
    
    def toggle_fullscreen(self, event=None):
        """Wechselt zwischen Vollbild und Fenster-Modus"""
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
        logger.debug(f"Vollbild: {'aktiviert' if self.fullscreen else 'deaktiviert'}")
    
    def exit_fullscreen(self, event=None):
        """Verlässt den Vollbild-Modus (aber bleibt auf Hauptmonitor)"""
        if self.fullscreen:
            self.fullscreen = False
            self.root.attributes('-fullscreen', False)
            self.root.attributes('-topmost', False)  # Topmost deaktivieren
            
            # Fenster auf Hauptmonitor in normaler Größe
            self.root.geometry(f"{self.primary_width}x{self.primary_height}+{self.primary_x}+{self.primary_y}")
            logger.debug("Vollbild deaktiviert - bleibt auf Hauptmonitor")
    
    def restart_application(self):
        """Startet die Anwendung neu"""
        logger.info("Anwendung wird neu gestartet...")
        subprocess.Popen([sys.executable] + sys.argv)
        self.quit_application()
    
    def quit_application(self):
        """Beendet die Anwendung"""
        logger.info("Anwendung wird beendet...")
        
        # Hardware-Verbindungen trennen
        from models.hardware import hardware_manager
        hardware_manager.disconnect_all()
        
        # Demo stoppen
        from services.demo import demo_service
        demo_service.stop_demo()
        
        # GUI schließen
        self.root.quit()
        sys.exit(0)
    
    def run(self):
        """Startet die GUI-Hauptschleife"""
        try:
            logger.info("GUI-Hauptschleife gestartet")
            self.root.mainloop()
        except KeyboardInterrupt:
            logger.info("Anwendung durch Benutzer unterbrochen")
            self.quit_application()
        except Exception as e:
            logger.error(f"Unerwarteter Fehler in GUI-Hauptschleife: {e}")
            self.quit_application()
